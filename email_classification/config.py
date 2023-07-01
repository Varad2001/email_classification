import os
from pathlib import Path

EMAIL_RANKER_MODEL_PATH = Path(f"{os.getcwd()}/email_classification/weights/weights.pkl")

EMAIL_API = "http://127.0.0.1:5000/get_emails"

