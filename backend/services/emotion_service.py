import cv2
import numpy as np
from tensorflow.keras.models import load_model
from config import Config
import logging
import os
import base64

# LOAD MODEL
model = None

try:
    if os.path.exists(Config.EMOTION_MODEL_PATH):
        model = load_model(Config.EMOTION_MODEL_PATH)
        print("✅ Emotion model loaded successfully")
    else:
        print("❌ Emotion model file NOT found")
except Exception as e:
    print("❌ Error loading emotion model:", e)


# LABELS
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]


# SESSION TRACKING
emotion_sessions = {}
FEAR_THRESHOLD = 5


# MAIN FUNCTION
def detect_emotion(image_input, user_id):
    try:
        print("\n📸 Emotion API called")
        print("User ID:", user_id)

        if model is None:
            print("❌ Model not loaded")
            return "Model Not Loaded"

        if user_id not in emotion_sessions:
            emotion_sessions[user_id] = 0

        # HANDLE INPUT (FILE OR BASE64)
        if hasattr(image_input, "read"):
            # FormData file
            file_bytes = np.frombuffer(image_input.read(), np.uint8)

        elif isinstance(image_input, str):
            # Base64 image
            img_data = base64.b64decode(image_input.split(",")[1])
            file_bytes = np.frombuffer(img_data, np.uint8)

        else:
            print("❌ Unsupported input format")
            return "Invalid Input"

        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            print("❌ Invalid image received")
            return "Invalid Image"

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # FACE DETECTION
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces) == 0:
            print("⚠ No face detected")
            return "No Face Detected"

        (x, y, w, h) = faces[0]

        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (48, 48))
        roi = roi / 255.0
        roi = np.reshape(roi, (1, 48, 48, 1))

        # PREDICTION
        prediction = model.predict(roi, verbose=0)
        emotion = emotion_labels[np.argmax(prediction)]

        print("😊 Predicted Emotion:", emotion)

        # AUTO SOS LOGIC
        if emotion == "Fear":
            emotion_sessions[user_id] += 1
        else:
            emotion_sessions[user_id] = 0

        if emotion_sessions[user_id] >= FEAR_THRESHOLD:
            emotion_sessions[user_id] = 0
            print("🚨 AUTO SOS TRIGGERED")
            logging.info(f"Auto-SOS triggered for user {user_id}")
            return "AUTO_SOS_TRIGGERED"

        return emotion

    except Exception as e:
        print("❌ Emotion Detection Error:", e)
        logging.error(f"Emotion Detection Error: {str(e)}")
        return "Detection Error"
