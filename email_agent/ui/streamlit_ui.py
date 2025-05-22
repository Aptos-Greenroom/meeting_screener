import streamlit as st
import time
import re
import os
from datetime import datetime
from PIL import Image
from agent.email_watcher import start_email_monitor, stop_email_monitor, resume_email_monitor
import threading

LOG_FILE_PATH = "logs/application.log"  # Path to the log file

# ---------- Streamlit Page Setup ----------
st.set_page_config(
    page_title="Z47 AI Email Agent Logs",
    layout="wide",
    page_icon="📩"
)

# ---------- Optional Branding ----------
# Uncomment if you have a logo image
# logo = Image.open("assets/logo.png")
# st.image(logo, width=150)

# ---------- Title and Description ----------
st.title("📩 Z47 AI Email Agent Logs")
st.caption("Send a mail to puneetshrivas32@gmail.com with the subject 'Company Summary Request' and either the name of the company or the website, the bot will respond with a report if the company is found. the bot will reply in ~ 1 minute with the report. Can keep replying with more requests  in the thread.")

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .log-box {
        background: #1e1e1e;
        color: #fff;
        padding: 1em;
        border-radius: 10px;
        height: 65vh;
        overflow-y: auto;
        font-family: monospace;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Layout Setup ----------
col1, col2 = st.columns([4, 1])

# ---------- Controls for Email Monitor ----------
with col2:
    st.subheader("⚙️ Controls")
    
    # Start/Stop Email Monitor Buttons
    if st.button("Start Agent"):
        resume_email_monitor() # Directly start the email monitor
        st.success("Email monitor started.")

    if st.button("Stop Agent"):
        stop_email_monitor()  # Directly stop the email monitor
        st.success("Email monitor stopped.")

    selected_level = st.selectbox("Log Level", ["ALL", "INFO", "WARNING", "ERROR", "DEBUG", "SYSTEM", "SUCCESS"])
    search_term = st.text_input("Search Term", placeholder="Type keyword...")

    with open(LOG_FILE_PATH, "r") as file:
        st.download_button("📥 Download Logs", file, file_name="application.log", mime="text/plain")

# ---------- Log Color Coding ----------
tag_colors = {
    "SYSTEM": "#00BFFF",
    "INFO": "#1E90FF",
    "DEBUG": "#8A2BE2",
    "SUCCESS": "#32CD32",
    "ERROR": "#FF6347",
    "WARNING": "#FFA500"
}
tag_pattern = re.compile(r"^\[(\w+)\]")

# ---------- Live Log Display ----------
with col1:
    st.subheader("🧾 Log Viewer")
    log_container = st.empty()

    def get_logs():
        logs = []
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as log_file:
                for msg in log_file.readlines():
                    tag_match = tag_pattern.match(msg)
                    tag = tag_match.group(1) if tag_match else "INFO"
                    if selected_level != "ALL" and tag != selected_level:
                        continue
                    if search_term and search_term.lower() not in msg.lower():
                        continue
                    color = tag_colors.get(tag, "#FFFFFF")
                    msg = msg.strip()
                    logs.append(f'<span style="color:{color}">{msg}</span>')
        return logs

    while True:
        logs = get_logs()
        log_container.markdown(
            f'<div class="log-box">{"<br>".join(logs[-200:])}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(1)
