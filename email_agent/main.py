import subprocess
import time
import agent.logging
from agent.email_watcher import start_email_monitor, stop_email_monitor
from workflow import start_ui
import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent.logging import log

LOG_FILE_PATH = "logs/application.log"  # Define the log file path

# Clear the log file at the start of the application
if os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, "w") as log_file:
        log_file.write("")  # Truncate the file

if __name__ == "__main__":
    log("Starting the application...", tag="INFO")
    print("[SYSTEM] Launching Streamlit UI in a separate process...")
    # Run Streamlit UI as a separate subprocess
    threading.Thread(target=start_ui, daemon=True).start()
    # # Start the email checking loop in a separate thread
    # email_monitor_thread = threading.Thread(target=start_email_monitor, daemon=True)
    # email_monitor_thread.start()
    start_email_monitor()
    try:
        # Example of running the application for a certain period
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        # Stop the email monitor when the application is interrupted
        stop_email_monitor()  # Stop the email monitor
        # email_monitor_thread.join()  # Wait for the thread to finish
        log("Email monitor stopped.", tag="INFO")

    log("Application finished successfully.", tag="SUCCESS")
