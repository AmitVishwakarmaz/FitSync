import cv2
import mediapipe as mp
import pandas as pd
import csv

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils  # For drawing keypoints
pose = mp_pose.Pose()

# Initialize CSV file
csv_file = 'exercise_data.csv'
header = [f"{joint}_{axis}" for joint in range(33) for axis in ['x', 'y', 'z']] + ['label']

# Open CSV for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

# Start webcam or video
cap = cv2.VideoCapture(0)  # Use 'video.mp4' for video file input

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to access the camera or video.")
        break

    # Convert to RGB for MediaPipe processing
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    # Convert back to BGR for OpenCV
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extract keypoints as a single row
        row = []
        for lm in landmarks:
            row.extend([lm.x, lm.y, lm.z])  # Add x, y, z coordinates of each landmark

        # Draw landmarks and connections on the image
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

        # Prompt for user input to label the frame
        cv2.putText(image, "Press 'c' for correct or 'i' for incorrect", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Pose Data Collection", image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            row.append("correct")  # Label the frame as correct
        elif key == ord('i'):
            row.append("incorrect")  # Label the frame as incorrect
        else:
            continue

        # Append row to CSV
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
