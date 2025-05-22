import subprocess
from agent.email_processor import process_email

def handle_email(uid, mail):
    return process_email(uid, mail)
def start_ui():
    subprocess.Popen(["python", "-m", "streamlit", "run", "C:/Users/punee/OneDrive/Documents/GitHub/meeting_screener/email_agent/ui/streamlit_ui.py"])
