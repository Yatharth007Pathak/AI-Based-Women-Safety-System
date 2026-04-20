# DISTRESS SOUND DETECTION TRAINING

import os
import numpy as np
import librosa
import joblib
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score


# DATASET PATH
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "audio_dataset")

# ===============================
# FEATURE EXTRACTION
# ===============================
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=3)

        mfcc = np.mean(
            librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T,
            axis=0
        )

        return mfcc

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


# LOAD DATASET
def load_data():

    features = []
    labels = []

    for label_folder in ["distress", "normal"]:
        folder_path = os.path.join(DATASET_PATH, label_folder)

        if not os.path.exists(folder_path):
            continue

        for file in os.listdir(folder_path):

            file_path = os.path.join(folder_path, file)

            feature = extract_features(file_path)

            if feature is not None:
                features.append(feature)

                if label_folder == "distress":
                    labels.append(1)
                else:
                    labels.append(0)

    return np.array(features), np.array(labels)


print("Loading audio dataset...")
X, y = load_data()

print(f"Total samples loaded: {len(X)}")


# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# TRAIN MODEL
print("Training model...")

model = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    activation="relu",
    solver="adam",
    max_iter=500,
    random_state=42
)

model.fit(X_train, y_train)


# EVALUATION
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# SAVE MODEL
joblib.dump(model, "sound_model.pkl")

print("\nModel saved as sound_model.pkl")
