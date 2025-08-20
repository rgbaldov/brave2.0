from adafruit_pca9685 import PCA9685
import board, busio

class MotorDriver:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50
    
    def set_servo_angle(self, channel, angle):
        pulse = int((angle/180)*400 + 150)
        self.pca.channels[channel].duty_cycle = pulse << 4

    def set_motor_speed(self, channel, speed):
        # speed: -1.0 to 1.0
        pulse = int((speed+1)/2 * 4095)
        self.pca.channels[channel].duty_cycle = pulse
