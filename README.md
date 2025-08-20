# BRAVE 2.0 Controls (new)

This project implements a new control design for the BRAVE robot powered by **NVIDIA Jetson Orin Nano**, equipped with **4×4K cameras**, RC capabilities, and **BLDC/servo motor drivers** for mobility and actuation. Note that the design does not include the _disruptor_ and _claw arm_ mechanism. The main program is still _in progress_. 

## ✨ Features
- Multi-camera (4×4K) video streaming - _**done with 1 camera setup using RPi4**_
- Remote control (keyboard, joystick, or web interface) - _**done using simulation and keyboard**_
- BLDC / Servo motor integration (PWM & fuzzy control) - _**done using simulation**_
- ROS2-ready modular architecture - _**on-going**_
- AI-ready for object detection and tracking (luggages, bag, and people) - _**on-going**_

## 📂 Project Structure
- `control/` → Motor drivers (PWN, fuzzy) & remote control
- `vision/` → Camera streaming & processing (almost same from 1st version but only 4 and without PTZ)
- `brave2.0_controls.pdf` → System architecture & power design

## 🛠️ Hardware Setup
- Jetson Orin Nano
- 4×4K USB/CSI cameras
- BLDC motors with ESCs or servo motors with PWM drivers (e.g., PCA9685)
- Power Supply: 24V battery → DC-DC converters (12V for motors, 5V for Jetson, 6V for servos)

## 📐 Conceptual Framework (Power & System Design)
- Power Distribution:
1. Battery Pack (24V Li-ion)
2. DC-DC Step Down 12V → BLDC Motors + ESCs
3. DC-DC Step Down 6V → Servo Motors (PCA9685)
4. DC-DC Step Down 5V/4A → Jetson Orin Nano + Cameras

<img width="1106" height="232" alt="brave_power" src="https://github.com/user-attachments/assets/9ed97946-3dc6-4912-99f6-f2dfc8453d65" />

- System Framework:
1. Jetson Orin Nano processes multi-camera input
2. User issues commands via RC (keyboard/web/joystick)
3. Jetson sends PWM/I2C commands to motor drivers (BLDC/servo)
4. Motors actuate robot accordingly

<img width="816" height="338" alt="brave_system" src="https://github.com/user-attachments/assets/5d5e81f9-c9ad-438b-b827-1b95f2ba1c92" />

