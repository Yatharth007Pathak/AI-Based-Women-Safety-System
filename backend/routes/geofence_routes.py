from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.geofence_service import check_high_risk_zone
from database.db import get_db_cursor
import logging

geofence_bp = Blueprint("geofence", __name__)


# CHECK GEO-FENCE RISK
@geofence_bp.route("/check", methods=["POST"])
@jwt_required()
def check_risk():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if not latitude or not longitude:
            return jsonify({"message": "Invalid location data"}), 400

        is_high_risk, risk_score, distance = check_high_risk_zone(
            float(latitude),
            float(longitude)
        )

        if is_high_risk:
            logging.info(f"GeoFence Alert for user {user_id}")

            # Log auto-alert
            connection, cursor = get_db_cursor()

            cursor.execute(
                """
                INSERT INTO alert_logs 
                (user_id, latitude, longitude, alert_type, risk_level)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, latitude, longitude, "GEOFENCE_AUTO", "HIGH")
            )

            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({
                "status": "HIGH_RISK_ZONE",
                "risk_score": risk_score,
                "distance_km": round(distance, 3),
                "auto_alert": True,
                "message": "You have entered a high-risk area"
            }), 200

        return jsonify({
            "status": "SAFE_ZONE",
            "risk_score": risk_score,
            "distance_km": round(distance, 3),
            "auto_alert": False
        }), 200

    except Exception as e:
        logging.error(f"GeoFence Error: {str(e)}")
        return jsonify({"message": "Geo-fence check failed"}), 500

# FETCH CRIME DATA FOR HEATMAP
@geofence_bp.route("/crime-data", methods=["GET"])
@jwt_required()
def get_crime_data():
    try:
        connection, cursor = get_db_cursor(dictionary=True)

        cursor.execute("""
            SELECT latitude, longitude, risk_score
            FROM crime_data
        """)

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify({"crime_data": data}), 200

    except Exception as e:
        logging.error(f"Crime Data Fetch Error: {str(e)}")
        return jsonify({"message": "Failed to fetch crime data"}), 500