from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
from services.sound_service import detect_sound
import logging

sound_bp = Blueprint("sound", __name__)

# SOUND DISTRESS DETECTION ROUTE
@sound_bp.route("/detect", methods=["POST"])
# @jwt_required()   # 🔥 DISABLED FOR DEMO
def sound_detect():
    try:
        # 🔥 Dummy user (since JWT disabled)
        user_id = 1

        if "audio" not in request.files:
            return jsonify({"message": "No audio file provided"}), 400

        audio = request.files["audio"]

        # Detect sound distress
        result = detect_sound(audio, user_id)

        return jsonify({
            "sound": result,
            "auto_alert": False
        }), 200

    except Exception as e:
        logging.error(f"Sound Detection Error: {str(e)}")
        return jsonify({"message": "Sound detection failed"}), 500
