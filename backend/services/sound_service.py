import librosa
import numpy as np
import joblib
import tempfile
import os
import logging
from config import Config

# LOAD MODEL
model = None

try:
    if os.path.exists(Config.SOUND_MODEL_PATH):
        model = joblib.load(Config.SOUND_MODEL_PATH)
        print("✅ Sound model loaded successfully")
    else:
        print("❌ Sound model file NOT found")
except Exception as e:
    print("❌ Error loading sound model:", e)


# SESSION TRACKING
sound_sessions = {}
DISTRESS_THRESHOLD = 2


# FEATURE EXTRACTION
def extract_features(file_path):
    try:
        print("🎧 Extracting audio features...")

        y, sr = librosa.load(file_path, sr=22050, mono=True)

        if y is None or len(y) == 0:
            print("❌ Empty audio file")
            return None, None

        # 🔥 VOLUME CALCULATION (IMPORTANT)
        volume = np.mean(np.abs(y))
        print("🔊 Volume:", volume)

        # Normalize
        if np.max(np.abs(y)) != 0:
            y = y / np.max(np.abs(y))

        # MFCC
        mfcc = np.mean(
            librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T,
            axis=0
        )

        return mfcc, volume

    except Exception as e:
        print("❌ Feature Extraction Error:", e)
        logging.error(f"Feature Extraction Error: {str(e)}")
        return None, None


# MAIN FUNCTION
def detect_sound(audio_file, user_id):
    try:
        print("\n🎤 Sound API called")
        print("User ID:", user_id)

        if user_id not in sound_sessions:
            sound_sessions[user_id] = 0

        # SAVE TEMP FILE
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            temp_path = tmp.name

        audio_file.stream.seek(0)
        with open(temp_path, "wb") as f:
            f.write(audio_file.read())

        print("📁 Temp audio saved:", temp_path)

        # EXTRACT FEATURES
        features, volume = extract_features(temp_path)

        # DELETE FILE
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # ❌ if totally failed
        if features is None:
            return "Normal"

        # 🔥 STEP 1: VOLUME BASED DETECTION (FAST + RELIABLE)
        if volume is not None and volume > 0.02:
            print("🚨 Loud sound detected")
            sound_sessions[user_id] += 1
            label = "Distress"
        else:
            # 🔥 STEP 2: ML MODEL (SECONDARY)
            if model is not None:
                prediction = model.predict(features.reshape(1, -1))
                result = int(prediction[0])
                print("🔊 ML Prediction:", result)

                if result == 1:
                    sound_sessions[user_id] += 1
                    label = "Distress"
                else:
                    sound_sessions[user_id] = 0
                    label = "Normal"
            else:
                label = "Normal"

        # AUTO SOS
        if sound_sessions[user_id] >= DISTRESS_THRESHOLD:
            sound_sessions[user_id] = 0
            print("🚨 AUTO SOS TRIGGERED")
            return "AUTO_SOS_TRIGGERED"

        return label

    except Exception as e:
        print("❌ Sound Detection Error:", e)
        logging.error(f"Sound Detection Error: {str(e)}")
        return "Detection Error"
