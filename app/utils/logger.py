import logging
from logging.handlers import RotatingFileHandler

LOG_FILE = "logs/app.log"

# Ensure logs directory exists
import os
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logger = logging.getLogger("event_backend")
logger.setLevel(logging.INFO)

# Rotating file handler for production logs
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
