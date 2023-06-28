import os
from datetime import datetime
import logging

LOG_FILE_NAME = f"{datetime.now().strftime('%d-%m-%Y__%H:%M:%S')}.log"

LOG_FILE_DIR = os.path.join(os.getcwd(), "logs")

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME)

# create folder if not available
os.makedirs(LOG_FILE_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format= "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s %(message)s",
    level=logging.INFO
)

