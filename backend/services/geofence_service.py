import math
import joblib
import os
from config import Config
import logging

# Load ML model
MODEL_PATH = "../ai_models/crime/crime_model.pkl"

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    logging.info("Crime prediction model loaded")
else:
    logging.warning("Crime model not found")


def haversine_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2)**2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def predict_risk(lat, lon):

    if model is None:
        return 0

    prediction = model.predict([[lat, lon]])

    return int(prediction[0])


def check_high_risk_zone(user_lat, user_lon):

    try:

        risk_score = predict_risk(user_lat, user_lon)

        # Convert prediction into zone type
        if risk_score >= 75:
            status = "HIGH_RISK_ZONE"
            is_high_risk = True
        elif risk_score >= 50:
            status = "MODERATE_RISK_ZONE"
            is_high_risk = False
        else:
            status = "SAFE_ZONE"
            is_high_risk = False

        return is_high_risk, risk_score, 0

    except Exception as e:
        logging.error(f"GeoFence ML Error: {str(e)}")
        return False, 0, 0