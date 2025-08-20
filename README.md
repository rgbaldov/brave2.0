# BRAVE 2.0 Controls (new)

This project implements a new control design for the BRAVE robot powered by **NVIDIA Jetson Orin Nano**, equipped with **4×4K cameras**, RC capabilities, and BLDC/servo motor drivers for mobility and actuation.  

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
   git clone https://github.com/yourusername/jetson-orin-robot.git
   cd jetson-orin-robot
