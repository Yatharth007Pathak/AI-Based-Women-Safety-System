from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.sound_service import detect_sound
from database.db import get_db_cursor
import logging

sound_bp = Blueprint("sound", __name__)

# SOUND DISTRESS DETECTION ROUTE
@sound_bp.route("/detect", methods=["POST"])
@jwt_required()
def sound_detect():
    try:
        user_id = get_jwt_identity()

        if "audio" not in request.files:
            return jsonify({"message": "No audio file provided"}), 400

        audio = request.files["audio"]

        # Detect sound distress
        result = detect_sound(audio, user_id)

        # If auto trigger happens
        if result == "AUTO_SOS_TRIGGERED":
            logging.info(f"Sound Auto-SOS triggered by user {user_id}")

            latitude = request.form.get("latitude")
            longitude = request.form.get("longitude")

            if latitude and longitude:
                connection, cursor = get_db_cursor()

                cursor.execute(
                    """
                    INSERT INTO alert_logs (user_id, latitude, longitude, alert_type, risk_level)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, latitude, longitude, "SOUND_AUTO", "HIGH")
                )

                connection.commit()
                cursor.close()
                connection.close()

            return jsonify({
                "sound_status": "Distress",
                "auto_alert": True,
                "message": "Auto SOS triggered due to repeated distress sound detection"
            }), 200

        return jsonify({
            "sound_status": result,
            "auto_alert": False
        }), 200

    except Exception as e:
        logging.error(f"Sound Detection Error: {str(e)}")
        return jsonify({"message": "Sound detection failed"}), 500