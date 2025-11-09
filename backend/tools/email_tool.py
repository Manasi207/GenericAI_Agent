# # # backend/tools/email_tool.py
# import os
# import smtplib
# from email.message import EmailMessage
# import re
# from dotenv import load_dotenv

# load_dotenv()

# SMTP_HOST = os.getenv("SMTP_HOST", "")
# SMTP_PORT = int(os.getenv("SMTP_PORT", "587") or 587)
# SMTP_USER = os.getenv("SMTP_USER", "")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
# EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER or "noreply@example.com")

# def _parse_input(payload: str):
#     """Parse semi-structured input into to/subject/body dict."""
#     parts = {}
#     for part in re.split(r";\s*", payload):
#         if ":" in part:
#             k, v = part.split(":", 1)
#             parts[k.strip().lower()] = v.strip()
#     return parts

# def send_email_tool(payload: str) -> str:
#     """
#     Send email using SMTP configuration from .env.
#     Expects: 'to:xyz@gmail.com; subject:Hello; body:Hi!'
#     """
#     if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD):
#         return "⚠️ SMTP not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD in .env."

#     parts = _parse_input(payload)
#     to = parts.get("to")
#     subject = parts.get("subject", "(no subject)")
#     body = parts.get("body", "")

#     # Try to find email address if 'to' is missing
#     if not to:
#         match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", payload)
#         if match:
#             to = match.group(1)

#     if not to:
#         return "❌ No recipient specified. Please include 'to:<email>' or a valid address."

#     msg = EmailMessage()
#     msg["From"] = EMAIL_FROM
#     msg["To"] = to
#     msg["Subject"] = subject
#     msg.set_content(body or "(No body)")

#     try:
#         with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=60) as smtp:
#             smtp.starttls()
#             smtp.login(SMTP_USER, SMTP_PASSWORD)
#             smtp.send_message(msg)
#         return f"✅ Email successfully sent to {to}!"
#     except smtplib.SMTPAuthenticationError:
#         return "❌ Authentication failed. Check SMTP_USER or SMTP_PASSWORD."
#     except smtplib.SMTPConnectError:
#         return "❌ Could not connect to SMTP server. Verify SMTP_HOST and PORT."
#     except Exception as e:
#         return f"❌ Failed to send email: {e}"
###########################################################################################

# backend/tools/email_tool.py - Simplified email tool (placeholder)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

def send_email_tool(to, subject, body):
    """Send a real email using SMTP credentials from .env"""
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM", smtp_user)

    if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
        return "❌ Missing SMTP configuration. Please check .env file."

    print("🔧 Preparing email...")
    print(f"FROM: {email_from} TO: {to}")

    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        print("📡 Connecting to SMTP server...")
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(smtp_user, smtp_password)
            response = server.send_message(msg)
            print("📨 Server response:", response)

        if response == {}:
            print("✅ Email sent successfully!")
            return f"✅ Email sent successfully to {to}"
        else:
            print("⚠️ Server returned non-empty response:", response)
            return f"⚠️ Email possibly not sent. Response: {response}"

    except smtplib.SMTPResponseException as e:
        print(f"❌ SMTP error: {e.smtp_code} - {e.smtp_error.decode()}")
        return f"❌ SMTP error: {e.smtp_code} - {e.smtp_error.decode()}"

    except Exception as e:
        print("❌ Exception while sending email:", e)
        print("🔍 Traceback:\n", traceback.format_exc())
        return f"❌ Error: {str(e)}"
