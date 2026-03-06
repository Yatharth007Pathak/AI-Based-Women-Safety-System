import librosa
import numpy as np
import joblib
import tempfile
import os
import logging
from config import Config


# Load Sound Model
try:
    if os.path.exists(Config.SOUND_MODEL_PATH):
        model = joblib.load(Config.SOUND_MODEL_PATH)
        logging.info("Sound model loaded successfully.")
    else:
        model = None
        logging.warning("Sound model file not found.")
except Exception as e:
    model = None
    logging.error(f"Error loading sound model: {str(e)}")


# Thread-safe session tracking per user
sound_sessions = {}

# Number of consecutive detections required
DISTRESS_THRESHOLD = 2


# Feature Extraction
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=3)

        # MFCC features
        mfcc = np.mean(
            librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T,
            axis=0
        )

        return mfcc

    except Exception as e:
        logging.error(f"Feature Extraction Error: {str(e)}")
        return None


# Sound Detection Function
def detect_sound(audio_file, user_id):
    try:
        if not model:
            return "Model Not Loaded"

        if user_id not in sound_sessions:
            sound_sessions[user_id] = 0

        # Save uploaded audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            temp_path = tmp.name

        # Extract features
        features = extract_features(temp_path)

        # Remove temporary file
        os.remove(temp_path)

        if features is None:
            return "Feature Extraction Failed"

        prediction = model.predict(features.reshape(1, -1))

        # Assuming model output: 1 = Distress, 0 = Normal
        if prediction[0] == 1:
            sound_sessions[user_id] += 1
        else:
            sound_sessions[user_id] = 0

        # Auto-SOS Logic
        if sound_sessions[user_id] >= DISTRESS_THRESHOLD:
            sound_sessions[user_id] = 0
            logging.info(f"Auto-SOS triggered via Sound for user {user_id}")
            return "AUTO_SOS_TRIGGERED"

        return "Distress Detected" if prediction[0] == 1 else "Normal"

    except Exception as e:
        logging.error(f"Sound Detection Error: {str(e)}")
        return "Detection Error"