import cv2
import mediapipe as mp
import csv

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils  # For drawing landmarks on the frame
pose = mp_pose.Pose()

# Open webcam
cap = cv2.VideoCapture(0)

# Open a CSV file to save data
with open("pose_data.csv", mode="a", newline="") as file:
    writer = csv.writer(file)
    # Write header: 99 keypoints (x, y, z for 33 landmarks) + 1 label
    header = [f"{coord}_{i}" for i in range(33) for coord in ("x", "y", "z")]
    header.append("label")
    writer.writerow(header)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Unable to access the camera.")
            break

        # Convert frame to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True

        # Check if landmarks are detected
        if results.pose_landmarks:
            # Draw the pose landmarks on the frame
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract keypoints
            landmarks = results.pose_landmarks.landmark
            keypoints = [lm.x for lm in landmarks] + [lm.y for lm in landmarks] + [lm.z for lm in landmarks]

            # Display keypoints on the frame
            for idx, lm in enumerate(landmarks):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.putText(frame, str(idx), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)

            # Add instructions
            cv2.putText(frame, "Press 'c' for Correct Pose, 'i' for Incorrect Pose, 'q' to Quit", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Save data based on key input
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):  # Correct Pose
                writer.writerow(keypoints + ["correct"])
                print("Correct pose saved.")
            elif key == ord("i"):  # Incorrect Pose
                writer.writerow(keypoints + ["incorrect"])
                print("Incorrect pose saved.")
            elif key == ord("q"):  # Quit
                break
        else:
            cv2.putText(frame, "No Pose Detected", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

        # Display the frame
        cv2.imshow("Pose Data Collection", frame)

cap.release()
cv2.destroyAllWindows()
