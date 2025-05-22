import time
import imaplib
from config import IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD
from workflow import handle_email
from agent.logging import log
import os

STATE_FILE = "email_monitor_state.txt"  # File to store the monitoring state

def read_monitoring_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            return file.read().strip() == "active"
    return False  # Default to inactive if the file does not exist

def write_monitoring_state(state):
    with open(STATE_FILE, "w") as file:
        file.write("active" if state else "inactive")

def check_inbox():
    # log("Checking inbox...", tag="INFO")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select('inbox')
    result, data = mail.uid('search', None, '(UNSEEN SUBJECT "Company Summary Request")')
    if result != 'OK':
        # log("No new emails.", tag="INFO")
        return

    uids = data[0].split()
    if(len(uids)>0):
        log(f"Found {len(uids)} new email(s).", tag="INFO")
        for uid in uids:
            handle_email(uid, mail)
    mail.logout()

def start_email_monitor():
    log("Starting email monitor...", tag="INFO")
    write_monitoring_state(True)  # Set state to active
    while True:  # Keep polling indefinitely
        if read_monitoring_state():  # Check if monitoring is active
            check_inbox()
            # log("Sleeping for 2 seconds...", tag="INFO")
            time.sleep(2)
        else:
            # log("Monitoring is inactive. Checking status again...", tag="INFO")
            time.sleep(2)  # Wait before checking the status again

def stop_email_monitor():
    log("Stopping email monitor...", tag="INFO")
    write_monitoring_state(False)  # Set state to inactive

def resume_email_monitor():
    log("Resuming email monitor...", tag="INFO")
    write_monitoring_state(True)  # Set state to active

