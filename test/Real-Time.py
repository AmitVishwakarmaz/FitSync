import cv2
import mediapipe as mp
import joblib
import numpy as np

# Load the trained model
model = joblib.load('exercise_form_model.pkl')

# Initialize MediaPipe Pose and Drawing
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Prediction function
def predict_form(keypoints):
    try:
        keypoints = np.array(keypoints).reshape(1, -1)
        return "correct" if model.predict(keypoints)[0] == 1 else "incorrect"
    except Exception as e:
        print(f"Error during prediction: {e}")
        return "unknown"

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Unable to access the camera.")
        break

    # Convert to RGB for MediaPipe processing
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True

    # Draw pose landmarks on the frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # Extract keypoints
        landmarks = results.pose_landmarks.landmark
        keypoints = [lm.x for lm in landmarks] + [lm.y for lm in landmarks] + [lm.z for lm in landmarks]

        # Predict form if keypoints match expected input size
        if len(keypoints) == 99:
            prediction = predict_form(keypoints)
            color = (0, 255, 0) if prediction == "correct" else (0, 0, 255)
            cv2.putText(frame, prediction.upper(), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Invalid Keypoints", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "No Pose Detected", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Add instructions for quitting
    cv2.putText(frame, "Press 'Q' to Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the frame
    cv2.imshow("Pose Detection", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
<<<<<<< HEAD

=======
print("hello world")
>>>>>>> ee4f58445654c3737139318750cc2f8a997ee2c7
cap.release()
cv2.destroyAllWindows()
