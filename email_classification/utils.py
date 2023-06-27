import time
from email.utils import parsedate


def extract_date_and_time(date_time):
    date_time = time.mktime(parsedate(date_time))
    return date_time

