import cv2
import numpy as np
from tensorflow.keras.models import load_model
from config import Config
import logging
import os


# Load Emotion Model
try:
    if os.path.exists(Config.EMOTION_MODEL_PATH):
        model = load_model(Config.EMOTION_MODEL_PATH)
        logging.info("Emotion model loaded successfully.")
    else:
        model = None
        logging.warning("Emotion model file not found.")
except Exception as e:
    model = None
    logging.error(f"Error loading emotion model: {str(e)}")


emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

# Thread-safe session tracking per user
emotion_sessions = {}

# Number of consecutive detections required for auto-SOS
FEAR_THRESHOLD = 5


# Emotion Detection Function
def detect_emotion(image_file, user_id):
    try:
        if not model:
            return "Model Not Loaded"

        if user_id not in emotion_sessions:
            emotion_sessions[user_id] = 0

        # Convert uploaded image to OpenCV format
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            return "Invalid Image"

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces) == 0:
            return "No Face Detected"

        # Process first detected face
        (x, y, w, h) = faces[0]

        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48, 48))
        roi = roi / 255.0
        roi = np.reshape(roi, (1, 48, 48, 1))

        prediction = model.predict(roi, verbose=0)
        emotion = emotion_labels[np.argmax(prediction)]

        # Auto-SOS Logic
        if emotion == "Fear":
            emotion_sessions[user_id] += 1
        else:
            emotion_sessions[user_id] = 0

        if emotion_sessions[user_id] >= FEAR_THRESHOLD:
            emotion_sessions[user_id] = 0
            logging.info(f"Auto-SOS triggered via Emotion for user {user_id}")
            return "AUTO_SOS_TRIGGERED"

        return emotion

    except Exception as e:
        logging.error(f"Emotion Detection Error: {str(e)}")
        return "Detection Error"