from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from database.db import get_db_cursor
import logging

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

# REGISTER ROUTE
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")

        # Basic validation
        if not full_name or not email or not password:
            return jsonify({"message": "Missing required fields"}), 400

        connection, cursor = get_db_cursor(dictionary=True)

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({"message": "User already exists"}), 409

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert user
        cursor.execute(
            """
            INSERT INTO users (full_name, email, password, phone)
            VALUES (%s, %s, %s, %s)
            """,
            (full_name, email, hashed_password, phone)
        )

        connection.commit()

        cursor.close()
        connection.close()

        logging.info(f"New user registered: {email}")

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        logging.error(f"Register Error: {str(e)}")
        return jsonify({"message": "Registration failed"}), 500


# LOGIN ROUTE
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Missing credentials"}), 400

        connection, cursor = get_db_cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Verify password
        if not bcrypt.check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid credentials"}), 401

        # Create JWT token
        access_token = create_access_token(identity=user["id"])

        logging.info(f"User logged in: {email}")

        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user_id": user["id"],
            "full_name": user["full_name"]
        }), 200

    except Exception as e:
        logging.error(f"Login Error: {str(e)}")
        return jsonify({"message": "Login failed"}), 500