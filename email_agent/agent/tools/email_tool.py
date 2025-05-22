import smtplib
import os
from email.message import EmailMessage
from config import EMAIL_ACCOUNT, EMAIL_PASSWORD, SMTP_SERVER
from agent.logging import log

def send_email_with_attachment(to, subject, body, filepath):
    log("Starting email processing", tag="INFO")
    if not os.path.exists(filepath):
        log("[ERROR] Attachment missing", tag="ERROR")
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = to
    msg.set_content(body)

    with open(filepath, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(filepath))

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        smtp.send_message(msg)
    log("Email processed successfully", tag="SUCCESS")

def send_error_email(to, subject, body):
    log("Starting error email processing", tag="INFO")
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = to
    msg.set_content(body)
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
        smtp.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        smtp.send_message(msg)
    log("Error Email processed successfully", tag="SUCCESS")

