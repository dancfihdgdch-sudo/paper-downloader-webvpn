import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# WebVPN Configuration
WEBVPN_URL = os.getenv('WEBVPN_URL', 'https://webvpn.hebmu.edu.cn')
WEBVPN_USERNAME = os.getenv('WEBVPN_USERNAME', '')
WEBVPN_PASSWORD = os.getenv('WEBVPN_PASSWORD', '')

# Download Configuration
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', './papers')
TIMEOUT = int(os.getenv('TIMEOUT', 30))
RETRY_TIMES = int(os.getenv('RETRY_TIMES', 3))

# Create download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
