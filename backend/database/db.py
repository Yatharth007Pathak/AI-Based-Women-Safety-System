import mysql.connector
from mysql.connector import Error
from config import Config
import logging


def get_db_connection():
    """
    Creates and returns a MySQL database connection.
    """

    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )

        if connection.is_connected():
            return connection

    except Error as e:
        logging.error(f"Database Connection Error: {str(e)}")
        raise e


def get_db_cursor(dictionary=False):
    """
    Returns a database cursor.
    If dictionary=True, returns results as dict instead of tuple.
    """

    connection = get_db_connection()

    if dictionary:
        return connection, connection.cursor(dictionary=True)

    return connection, connection.cursor()