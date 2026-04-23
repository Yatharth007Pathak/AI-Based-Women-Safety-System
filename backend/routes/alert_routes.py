from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import get_db_cursor
from services.alert_service import send_sos_alert
import logging

alert_bp = Blueprint("alerts", __name__)


# MANUAL SOS TRIGGER
@alert_bp.route("/sos", methods=["POST"])
@jwt_required()
def manual_sos():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not latitude or not longitude:
            return jsonify({"message": "Invalid location data"}), 400

        # Log alert in database
        connection, cursor = get_db_cursor()

        cursor.execute(
            """
            INSERT INTO alert_logs (user_id, latitude, longitude, alert_type, risk_level)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, latitude, longitude, "MANUAL_SOS", "HIGH")
        )

        connection.commit()
        cursor.close()
        connection.close()

        # Send SMS & Email
        send_sos_alert(user_id, latitude, longitude)

        logging.info(f"Manual SOS triggered by user {user_id}")

        return jsonify({"message": "Emergency alert sent successfully"}), 200

    except Exception as e:
        logging.error(f"SOS Error: {str(e)}")
        return jsonify({"message": "Failed to trigger SOS"}), 500


# AUTO ALERT (Emotion / Sound / GeoFence)
@alert_bp.route("/auto-alert", methods=["POST"])
@jwt_required()
def auto_alert():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        trigger_type = data.get("trigger_type")  # EMOTION / SOUND / GEOFENCE

        if not latitude or not longitude or not trigger_type:
            return jsonify({"message": "Invalid request"}), 400

        # Log alert
        connection, cursor = get_db_cursor()

        cursor.execute(
            """
            INSERT INTO alert_logs (user_id, latitude, longitude, alert_type, risk_level)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, latitude, longitude, trigger_type, "HIGH")
        )

        connection.commit()
        cursor.close()
        connection.close()

        # Send alert
        send_sos_alert(user_id, latitude, longitude)

        logging.info(f"Auto alert triggered by user {user_id} via {trigger_type}")

        return jsonify({"message": "Auto emergency alert sent"}), 200

    except Exception as e:
        logging.error(f"Auto Alert Error: {str(e)}")
        return jsonify({"message": "Auto alert failed"}), 500


# GET USER ALERT HISTORY
@alert_bp.route("/history", methods=["GET"])
@jwt_required()
def get_alert_history():
    try:
        user_id = get_jwt_identity()

        connection, cursor = get_db_cursor(dictionary=True)

        cursor.execute(
            """
            SELECT latitude, longitude, alert_type, risk_level, created_at
            FROM alert_logs
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        alerts = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"alerts": alerts}), 200

    except Exception as e:
        logging.error(f"Fetch Alert History Error: {str(e)}")
        return jsonify({"message": "Failed to fetch alert history"}), 500
