""" Helper functions for chat """
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday


def calculate_time(timestamp):
    """
    1. Today or yesterday:
        - EX: today at 10:56 AM
    2. Other days:
        - EX: 12/28/2020 at 7:31 PM
    """
    ts = ""
    # Today or yesterday
    day = naturalday(timestamp)
    if (day == "today") or (day == "yesterday"):
        # Get time - EX: 1:01 PM
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        # Create timestamp including day and time
        ts = f"{day} at {str_time}"
    # Other days - not sure if time AM/PM working
    else:
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        str_date = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_date} at {str_time}"
    return str(ts)
