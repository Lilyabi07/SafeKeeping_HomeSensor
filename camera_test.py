# Bianca Bien-Aime - 1932648 

#CAMERA_TEST
from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.start()
print("Camera started. Press 'q' to quit.")

while True:
    frame = picam2.capture_array()
    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
