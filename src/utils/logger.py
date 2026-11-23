import logging
import os
from datetime import datetime

LOG_DIR = "data/logs"

os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(
    LOG_DIR,
    f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AI_Intelligence_Hub")


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)


def log_warning(message):
    logger.warning(message)