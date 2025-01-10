import cv2
import mediapipe as mp
import joblib
import numpy as np

# Load the trained model
model = joblib.load('exercise_form_model.pkl')

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Predict form based on new data
def predict_form(keypoints):
    # Ensure keypoints are in the correct shape for the model
    keypoints = np.array(keypoints).reshape(1, -1)
    prediction = model.predict(keypoints)
    return prediction[0]

# Start webcam or video capture
cap = cv2.VideoCapture(0)  # Use webcam or replace with video path if needed

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to access the camera or video.")
        break

    # Convert the frame to RGB for MediaPipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    # Convert the frame back to BGR for OpenCV display
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Process pose landmarks
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        keypoints = []
        for lm in landmarks:
            keypoints.extend([lm.x, lm.y, lm.z])  # Append x, y, z coordinates for all landmarks

        # Ensure the number of keypoints matches the model input
        if len(keypoints) == 99:  # 33 landmarks × 3 coordinates
            prediction = predict_form(keypoints)
            if prediction == "correct":
                cv2.putText(image, "Correct Form", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                cv2.putText(image, "Incorrect Form", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            print("Invalid keypoints detected. Ensure proper form and try again.")
    else:
        print("No landmarks detected.")

    # Display the output
    cv2.imshow("Pose Detection", image)

    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
