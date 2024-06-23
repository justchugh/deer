import cv2
import time

cap = cv2.VideoCapture(0)
while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Video Stream', frame)
        print(f"Capture Time: {time.time() - start_time:.4f} s")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
