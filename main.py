import cv2
import mediapipe as mp
import threading

# --- MediaPipe setup ---
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# --- IP Webcam stream URLs ---
url1 = "http://100.100.245.98:8080/video"  # Kamera 1
url2 = "http://10.212.180.205:8080/video"  # Kamera 2 (ZMIEN NA WLASNY ADRES)

cap1 = cv2.VideoCapture(url1)
cap2 = cv2.VideoCapture(url2)

if not cap1.isOpened():
    print("Nie można otworzyć strumienia: Kamera 1")
    exit()

if not cap2.isOpened():
    print("Nie można otworzyć strumienia: Kamera 2")
    exit()

# --- Shared variables ---
frame1 = None
frame2 = None
results1 = None
results2 = None
running = True

# --- Function to process a camera ---
def process_camera(cap, pose_instance, frame_holder, results_holder):
    global running
    while running:
        ret, frame = cap.read()
        if not ret:
            print("Nie można pobrać klatki z kamery!")
            running = False
            break
        frame_holder[0] = frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_holder[0] = pose_instance.process(rgb)

# Holders for frames and results (mutable)
frame1_holder = [None]
frame2_holder = [None]
results1_holder = [None]
results2_holder = [None]

# --- Create separate Pose instances ---
pose1 = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

pose2 = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --- Start threads for each camera ---
thread1 = threading.Thread(target=process_camera, args=(cap1, pose1, frame1_holder, results1_holder))
thread2 = threading.Thread(target=process_camera, args=(cap2, pose2, frame2_holder, results2_holder))

thread1.start()
thread2.start()

# --- Main loop for displaying frames ---
while running:
    if frame1_holder[0] is not None:
        frame1 = frame1_holder[0].copy()
        if results1_holder[0] and results1_holder[0].pose_landmarks:
            mp_drawing.draw_landmarks(
                frame1,
                results1_holder[0].pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(thickness=2)
            )
        cv2.imshow("Kamera 1 + Skeleton", frame1)

    if frame2_holder[0] is not None:
        frame2 = frame2_holder[0].copy()
        if results2_holder[0] and results2_holder[0].pose_landmarks:
            mp_drawing.draw_landmarks(
                frame2,
                results2_holder[0].pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(thickness=2)
            )
        cv2.imshow("Kamera 2 + Skeleton", frame2)

    # Exit on ESC
    if cv2.waitKey(1) == 27:
        running = False
        break

# --- Cleanup ---
thread1.join()
thread2.join()
pose1.close()
pose2.close()
cap1.release()
cap2.release()
cv2.destroyAllWindows()
