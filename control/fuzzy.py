import math
import time

def clamp(x, lo, hi): 
    return max(lo, min(hi, x))

def tri(x, a, b, c):
    """Triangular membership."""
    if x <= a or x >= c: return 0.0
    if x == b: return 1.0
    if x < b: return (x - a) / (b - a)
    return (c - x) / (c - b)

def trap(x, a, b, c, d):
    """Trapezoidal membership."""
    if x <= a or x >= d: return 0.0
    if b <= x <= c: return 1.0
    if a < x < b: return (x - a) / (b - a)
    return (d - x) / (d - c)

class FuzzyController:
    """
    Fuzzy throttle controller:
      Inputs:  v_err (v_cmd - v_meas), dv_err (delta of v_err)
      Output:  throttle_norm in [-1, 1]  (positive = forward)
    Fuzzy steering controller:
      Input:   w_cmd (angular vel command)
      Output:  steer_norm in [-1, 1]     (left negative or positive -> map as needed)
    """

    def __init__(self,
                 v_max=1.5, w_max=1.5,
                 sample_time=0.05,
                 throttle_limit=1.0,
                 steer_limit=1.0):
        self.v_max = float(v_max)
        self.w_max = float(w_max)
        self.dt = float(sample_time)
        self.throttle_limit = float(throttle_limit)
        self.steer_limit = float(steer_limit)

        self._prev_v_err = 0.0
        self._last_t = time.time()

        # Output universe centers (defuzz) for throttle
        # StrongBrake < Brake < Zero < Push < StrongPush
        self._throttle_levels = {
            "SB": -1.0,   # strong brake/reverse
            "B":  -0.4,   # mild brake
            "Z":   0.0,   # coast
            "P":   0.4,   # push/accelerate
            "SP":  1.0    # strong push
        }

        # Steering defuzz centers
        # HardLeft < Left < Zero < Right < HardRight
        self._steer_levels = {
            "HL": -1.0,
            "L":  -0.4,
            "Z":   0.0,
            "R":   0.4,
            "HR":  1.0
        }

    # -------- Memberships --------
    def _memb_v_err(self, e):
        # normalize to [-1,1] by v_max
        x = clamp(e / (self.v_max + 1e-9), -1.5, 1.5)
        return {
            "NL": trap(x, -1.5, -1.0, -0.7, -0.4),  # Negative Large
            "NS": tri(x, -0.8, -0.4, 0.0),          # Negative Small
            "ZE": trap(x, -0.2, -0.05, 0.05, 0.2),  # Zero
            "PS": tri(x, 0.0, 0.4, 0.8),            # Positive Small
            "PL": trap(x, 0.4, 0.7, 1.0, 1.5)       # Positive Large
        }

    def _memb_dv_err(self, de):
        # normalize to [-1,1] roughly (rate of change)
        x = clamp(de / (self.v_max + 1e-9), -1.5, 1.5)
        return {
            "NF": trap(x, -1.5, -1.0, -0.6, -0.2),  # Negative Fast (error dropping quickly)
            "NS": tri(x, -0.5, -0.25, 0.0),         # Negative Slow
            "ZE": trap(x, -0.1, -0.03, 0.03, 0.1),  # Zero
            "PS": tri(x, 0.0, 0.25, 0.5),           # Positive Slow
            "PF": trap(x, 0.2, 0.6, 1.0, 1.5)       # Positive Fast (error rising quickly)
        }

    def _memb_w_cmd(self, w):
        x = clamp(w / (self.w_max + 1e-9), -1.5, 1.5)
        return {
            "HL": trap(x, -1.5, -1.0, -0.8, -0.5),
            "L":  tri(x, -0.8, -0.4, -0.05),
            "Z":  trap(x, -0.1, -0.03, 0.03, 0.1),
            "R":  tri(x, 0.05, 0.4, 0.8),
            "HR": trap(x, 0.5, 0.8, 1.0, 1.5)
        }

    # -------- Rules --------
    # Throttle rules (Mamdani): if v_err is ... and dv_err is ... then throttle is ...
    # Intuition:
    # - If we’re too slow (PL) and error growing (PF), push strongly (SP).
    # - If we’re too fast (NL) and error growing negative (PF on negative), brake strongly (SB).
    # - Near zero error -> coast.
    def _throttle_rulebase(self, E, dE):
        # Get membership dicts
        me = self._memb_v_err(E)
        mde = self._memb_dv_err(dE)

        rules = []
        # A small helper for rule creation
        def R(mu, label): rules.append((mu, label))

        # --- Core rules ---
        # Too fast (negative error): brake
        R(min(me["NL"], mde["PF"]), "SB")
        R(min(me["NL"], mde["PS"]), "SB")
        R(min(me["NL"], mde["ZE"]), "B")
        R(min(me["NS"], mde["PF"]), "B")
        R(min(me["NS"], mde["PS"]), "B")
        R(min(me["NS"], mde["ZE"]), "B")

        # Good/near target: coast
        R(min(me["ZE"], mde["ZE"]), "Z")
        R(min(me["ZE"], mde["NS"]), "Z")
        R(min(me["ZE"], mde["PS"]), "Z")

        # Too slow (positive error): push
        R(min(me["PS"], mde["ZE"]), "P")
        R(min(me["PS"], mde["NS"]), "P")
        R(min(me["PS"], mde["NF"]), "P")
        R(min(me["PL"], mde["ZE"]), "SP")
        R(min(me["PL"], mde["NS"]), "SP")
        R(min(me["PL"], mde["NF"]), "SP")

        # Aggregate by max for each label
        agg = {k: 0.0 for k in ["SB", "B", "Z", "P", "SP"]}
        for mu, label in rules:
            agg[label] = max(agg[label], mu)
        return agg

    # Steering rules: direct fuzzy mapping from w_cmd
    def _steer_rulebase(self, W):
        mw = self._memb_w_cmd(W)
        agg = {k: 0.0 for k in ["HL", "L", "Z", "R", "HR"]}
        for k in agg:
            agg[k] = mw[k]
        return agg

    # -------- Defuzzification (COG over singleton outputs) --------
    def _defuzz_singleton(self, agg, centers: dict, limit):
        num = 0.0
        den = 0.0
        for label, mu in agg.items():
            c = centers[label]
            num += mu * c
            den += mu
        out =
