import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
data_path = "pose_data.csv"
try:
    data = pd.read_csv(data_path)
    print(f"Dataset loaded successfully from {data_path}.")
except FileNotFoundError:
    print(f"Error: File {data_path} not found. Please ensure the file exists.")
    exit()

# Check if dataset is valid
if "label" not in data.columns:
    print("Error: The dataset must contain a 'label' column.")
    exit()

# Inspect and clean label column
valid_labels = ["correct", "incorrect"]
invalid_labels = data[~data["label"].isin(valid_labels)]
if not invalid_labels.empty:
    print("Invalid labels found:")
    print(invalid_labels)
    data = data[data["label"].isin(valid_labels)]  # Remove invalid labels
    print("Invalid labels have been removed.")

# Split features and labels
X = data.drop(columns=["label"])
y = data["label"]

# Encode labels (if they are strings)
label_mapping = {"correct": 1, "incorrect": 0}
if y.dtypes == object:  # Only map if labels are strings
    y = y.map(label_mapping)

# Validate data integrity
if y.isnull().any():
    print("Error: Some labels could not be encoded. Check the dataset for invalid labels.")
    exit()

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Data split into training and testing sets (Train: {len(X_train)}, Test: {len(X_test)}).")

# Train the model
print("Training the Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("Model training complete.")

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\nModel Evaluation:")
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["incorrect", "correct"]))

# Save the trained model
model_path = "exercise_form_model.pkl"
joblib.dump(model, model_path)
print(f"\nModel saved as {model_path}.")
