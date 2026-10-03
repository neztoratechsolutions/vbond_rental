import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


load_dotenv()


MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

MAIL_PORT = int(
    os.getenv("MAIL_PORT", "587")
)

MAIL_SERVER = os.getenv(
    "MAIL_SERVER",
    "smtp.gmail.com"
)


def send_otp_email(
    recipient_email: str,
    otp: str
):
    message = MIMEMultipart()

    message["From"] = MAIL_FROM
    message["To"] = recipient_email
    message["Subject"] = "Rental App - Password Reset OTP"

    body = f"""
Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for 5 minutes.

If you did not request a password reset, please ignore this email.

Regards,
Rental App Team
"""

    message.attach(
        MIMEText(body, "plain")
    )

    try:
        with smtplib.SMTP(
            MAIL_SERVER,
            MAIL_PORT,
            timeout=30
        ) as server:

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(
                MAIL_USERNAME,
                MAIL_PASSWORD
            )

            server.sendmail(
                MAIL_FROM,
                recipient_email,
                message.as_string()
            )

    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Authentication Error:", e)
        raise

    except smtplib.SMTPException as e:
        print("SMTP Error:", e)
        raise

    except Exception as e:
        print("Email Error:", e)
        raise