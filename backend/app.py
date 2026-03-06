from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging

# Import configuration
from config import Config

# Import blueprints
from routes.auth_routes import auth_bp
from routes.alert_routes import alert_bp
from routes.emotion_routes import emotion_bp
from routes.sound_routes import sound_bp
from routes.geofence_routes import geofence_bp

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Enable CORS for frontend communication
    CORS(app)

    # Initialize JWT
    jwt = JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(alert_bp, url_prefix="/api/alerts")
    app.register_blueprint(emotion_bp, url_prefix="/api/emotion")
    app.register_blueprint(sound_bp, url_prefix="/api/sound")
    app.register_blueprint(geofence_bp, url_prefix="/api/geofence")

    # Logging Configuration
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Health Check Route
    @app.route("/")
    def health_check():
        return jsonify({
            "status": "running",
            "message": "AI-Based Women Safety Analytics Backend is active"
        })

    # JWT Error Handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({"message": "Missing Authorization Header"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({"message": "Invalid Token"}), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token Expired"}), 401

    # Global Error Handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Unhandled Exception: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error"
        }), 500

    return app

# Run Application
if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG)