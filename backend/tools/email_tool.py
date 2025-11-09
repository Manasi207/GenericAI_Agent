
###########################################################################################

# backend/tools/email_tool.py - Simplified email tool (placeholder)

import os
import smtplib
from email.message import EmailMessage
import re
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587") or 587)
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER or "noreply@example.com")

def _parse_input(payload: str):
    parts = {}
    for part in re.split(r";\s*", payload):
        if ":" in part:
            k, v = part.split(":", 1)
            parts[k.strip().lower()] = v.strip()
    return parts

def send_email_tool(payload: str) -> str:
    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD):
        return "⚠️ SMTP not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASSWORD in .env."

    parts = _parse_input(payload)
    to = parts.get("to")
    subject = parts.get("subject", "(no subject)")
    body = parts.get("body", "")

    if not to:
        match = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", payload)
        if match:
            to = match.group(1)
    if not to:
        return "❌ No recipient specified. Please include 'to:<email>' or a valid address."

    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body or "(No body)")

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=60) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)
        return f"✅ Email successfully sent to {to}!"
    except smtplib.SMTPAuthenticationError:
        return "❌ Authentication failed. Check SMTP_USER or SMTP_PASSWORD."
    except smtplib.SMTPConnectError:
        return "❌ Could not connect to SMTP server."
    except Exception as e:
        return f"❌ Failed to send email: {e}"
