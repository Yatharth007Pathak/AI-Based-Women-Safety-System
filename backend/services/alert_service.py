from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from config import Config
from database.db import get_db_cursor
import logging


# Initialize Twilio Client
client = None
if Config.TWILIO_ACCOUNT_SID and Config.TWILIO_AUTH_TOKEN:
    client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)


# Send SMS via Twilio
def send_sms(phone_number, message):
    try:
        if not client:
            logging.warning("Twilio client not configured.")
            return

        client.messages.create(
            body=message,
            from_=Config.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        logging.info(f"SMS sent to {phone_number}")

    except Exception as e:
        logging.error(f"SMS Sending Error: {str(e)}")


# Send Email via SMTP
def send_email(to_email, subject, body):
    try:
        if not Config.EMAIL_ADDRESS or not Config.EMAIL_PASSWORD:
            logging.warning("Email configuration missing.")
            return

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = Config.EMAIL_ADDRESS
        msg["To"] = to_email

        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
        server.sendmail(Config.EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()

        logging.info(f"Email sent to {to_email}")

    except Exception as e:
        logging.error(f"Email Sending Error: {str(e)}")


# Send SOS Alert (SMS + Email)
def send_sos_alert(user_id, latitude, longitude):
    try:
        location_link = f"https://maps.google.com/?q={latitude},{longitude}"

        message = (
            "🚨 EMERGENCY ALERT 🚨\n\n"
            "User is in danger.\n"
            f"Live Location:\n{location_link}\n\n"
            "Please take immediate action."
        )

        # Fetch emergency contacts
        connection, cursor = get_db_cursor(dictionary=True)

        cursor.execute(
            "SELECT contact_name, contact_phone FROM emergency_contacts WHERE user_id = %s",
            (user_id,)
        )

        contacts = cursor.fetchall()

        cursor.close()
        connection.close()

        if not contacts:
            logging.warning(f"No emergency contacts found for user {user_id}")
            return

        # Send SMS to each contact
        for contact in contacts:
            send_sms(contact["contact_phone"], message)

        # Optional: Send email to primary email address
        if Config.EMAIL_ADDRESS:
            send_email(
                Config.EMAIL_ADDRESS,
                "Emergency Alert Notification",
                message
            )

        logging.info(f"SOS alerts sent for user {user_id}")

    except Exception as e:
        logging.error(f"SOS Alert Error: {str(e)}")