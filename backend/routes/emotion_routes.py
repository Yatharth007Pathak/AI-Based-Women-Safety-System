from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.emotion_service import detect_emotion
from database.db import get_db_cursor
import logging

emotion_bp = Blueprint("emotion", __name__)


# ==========================================
# EMOTION DETECTION ROUTE
# ==========================================
@emotion_bp.route("/detect", methods=["POST"])
@jwt_required()
def emotion_detect():
    try:
        user_id = get_jwt_identity()

        if "image" not in request.files:
            return jsonify({"message": "No image file provided"}), 400

        image = request.files["image"]

        # Detect emotion
        result = detect_emotion(image, user_id)

        # If auto trigger happens
        if result == "AUTO_SOS_TRIGGERED":
            logging.info(f"Emotion Auto-SOS triggered by user {user_id}")

            # Log into database
            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")

            if latitude and longitude:
                connection, cursor = get_db_cursor()

                cursor.execute(
                    """
                    INSERT INTO alert_logs (user_id, latitude, longitude, alert_type, risk_level)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, latitude, longitude, "EMOTION_AUTO", "HIGH")
                )

                connection.commit()
                cursor.close()
                connection.close()

            return jsonify({
                "emotion": "Fear",
                "auto_alert": True,
                "message": "Auto SOS triggered due to continuous fear detection"
            }), 200

        return jsonify({
            "emotion": result,
            "auto_alert": False
        }), 200

    except Exception as e:
        logging.error(f"Emotion Detection Error: {str(e)}")
        return jsonify({"message": "Emotion detection failed"}), 500