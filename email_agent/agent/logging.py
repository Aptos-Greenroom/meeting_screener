# agent/logging.py
import os

LOG_FILE_PATH = "logs/application.log"  # Define the log file path

def log(message: str, tag="INFO"):
    tagged_msg = f"[{tag}] {message}"
    
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    # Write the log message to the file
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(tagged_msg + "\n")
    
    print(tagged_msg)  # Show in terminal
