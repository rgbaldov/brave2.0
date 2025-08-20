# BRAVE 2.0 Controls (new)

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
