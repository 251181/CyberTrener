import cv2

# Replace with your phone's IP address
url = "http://10.211.57.174:8080/video"
video_capture = cv2.VideoCapture(url)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("IP Webcam stream", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
