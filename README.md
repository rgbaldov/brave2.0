<img width="1880" height="1118" alt="conceptual_framework" src="https://github.com/user-attachments/assets/ce535f87-f6ef-4133-bd94-ca47e7bbe2d4" /># BRAVE 2.0 Controls (new)

This project implements a new control design for the BRAVE robot powered by **NVIDIA Jetson Orin Nano**, equipped with **4×4K cameras**, RC capabilities, and **BLDC/servo motor drivers** for mobility and actuation.  

## ✨ Features
- Multi-camera (4×4K) video streaming
- Remote control (keyboard, joystick, or web interface)
- BLDC / Servo motor integration
- ROS2-ready modular architecture
- AI-ready for object detection and tracking

## 📂 Project Structure
- `vision/` → Camera streaming & processing
- `control/` → Motor drivers & remote control
- `robot_main.py` → Main program
- `docs/` → System architecture & power design

## 🚀 Getting Started
1. Clone repo:
   ```bash
   git clone https://github.com/rgbaldov/brave2.0.git
   cd brave2.0
2. Install requirements:
    ```bash
   pip install -r requirements.txt
3. Install requirements:
    ```bash
   python3 brave2.py

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

<img width="810" height="336" alt="brave_system" src="https://github.com/user-attachments/assets/0fc655c5-cb79-4dc8-a10c-7180acd42ef9" />
