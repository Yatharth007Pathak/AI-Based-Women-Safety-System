from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
from services.emotion_service import detect_emotion
import logging

emotion_bp = Blueprint("emotion", __name__)


@emotion_bp.route("/predict", methods=["POST"])
# @jwt_required()   # 🔥 DISABLED FOR DEMO
def emotion_detect():
    try:
        # 🔥 Dummy user (since JWT disabled)
        user_id = 1

        data = request.json.get("image")

        if not data:
            return jsonify({"message": "No image data provided"}), 400

        # 🔥 DIRECTLY PASS BASE64 STRING
        result = detect_emotion(data, user_id)

        return jsonify({
            "emotion": result,
            "auto_alert": False
        }), 200

    except Exception as e:
        logging.error(f"Emotion Detection Error: {str(e)}")
        return jsonify({"message": "Emotion detection failed"}), 500
