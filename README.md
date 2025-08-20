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

### Multi-Camera Streaming (`vision/camera_stream.py`)
```python
import cv2

def start_cameras(camera_ids=[0,1,2,3]):
    caps = [cv2.VideoCapture(i) for i in camera_ids]
    while True:
        frames = []
        for cap in caps:
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        combined = cv2.hconcat(frames)
        cv2.imshow("4K Multi-Camera View", combined)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    start_cameras()


### Multi-Camera Streaming (`control/motor_driver.py`)
```python
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
