import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email account credentials
IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# API keys
AFFINITY_API_KEY = os.getenv('AFFINITY_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Affinity API
AFFINITY_BASE_URL = 'https://api.affinity.co'
