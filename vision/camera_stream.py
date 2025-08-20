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
