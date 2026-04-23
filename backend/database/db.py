import mysql.connector
from config import Config
import logging


def get_db_connection():
    """
    Creates and returns a MySQL database connection
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="gp944cawm66",
            database="women_safety_db"
        )

        if connection.is_connected():
            return connection
        else:
            return None

    except Exception as e:
        print("Database connection error:", e)
        return None


def get_db_cursor(dictionary=False):
    """
    Returns a database cursor.
    If dictionary=True, returns results as dict instead of tuple.
    """

    connection = get_db_connection()

    # safety check
    if connection is None:
        print("Connection failed")
        return None, None

    if dictionary:
        return connection, connection.cursor(dictionary=True)

    return connection, connection.cursor()
