import cv2
import mediapipe as mp
import pandas as pd
import csv

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# CSV file to save the dataset
csv_file = 'exercise_data1.csv'
header = [f"{joint}_{axis}" for joint in range(33) for axis in ['x', 'y', 'z']] + ['label']

# Create the CSV file and write the header
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

# Start capturing video
cap = cv2.VideoCapture(0)  # Use webcam (or replace with a video file path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to access the camera or video.")
        break

    # Convert to RGB for MediaPipe processing
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    # Convert back to BGR for OpenCV display
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Extract keypoints
        row = []
        for lm in landmarks:
            row.extend([lm.x, lm.y, lm.z])

        # Display instructions
        cv2.putText(image, "Press 'c' for Correct, 'i' for Incorrect", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Pose Data Collection", image)

        # Get user input for labeling
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            row.append("correct")
        elif key == ord('i'):
            row.append("incorrect")
        else:
            continue

        # Save the row to the CSV
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp
# import pandas as pd
# import numpy as np

# mp_pose = mp.solutions.pose

# # Load the dataset
# csv_file = 'exercise_data.csv'
# data = pd.read_csv(csv_file)

# # Extract "correct" keypoints from the dataset for comparison
# correct_poses = data[data['label'] == 'correct'].iloc[:, :-1].values.reshape(-1, 33, 3)

# # Function to determine correctness of a pose
# def is_pose_correct(detected_keypoints, correct_poses, tolerance=0.05):
#     for correct_pose in correct_poses:
#         matches = []
#         for i, joint in enumerate(detected_keypoints):
#             if np.all(np.abs(joint - correct_pose[i]) <= tolerance):
#                 matches.append(True)
#             else:
#                 matches.append(False)
#         if all(matches):
#             return True
#     return False

# # Initialize MediaPipe Pose\mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()
# mp_drawing = mp.solutions.drawing_utils

# # Open the camera
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture frame")
#         break

#     # Convert the frame to RGB
#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     image.flags.writeable = False

#     # Process the image and detect pose
#     results = pose.process(image)

#     # Draw the pose annotations on the frame
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#     if results.pose_landmarks:
#         mp_drawing.draw_landmarks(
#             image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

#         # Extract the pose landmarks
#         landmarks = results.pose_landmarks.landmark
#         detected_keypoints = np.array(
#             [[landmark.x, landmark.y, landmark.z] for landmark in landmarks]
#         )

#         # Check if the pose is correct
#         if is_pose_correct(detected_keypoints, correct_poses):
#             cv2.putText(image, 'Correct Pose', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#         else:
#             cv2.putText(image, 'Incorrect Pose', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

#     # Display the frame
#     cv2.imshow('Pose Detection', image)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()
