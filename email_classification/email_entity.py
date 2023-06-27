from dataclasses import dataclass
from datetime import datetime

@dataclass
class Email :
    #email_path : str
    sender_email_address : str
    subject : str
    contents : str
    date_time : datetime
    rank = 0
    url : str
