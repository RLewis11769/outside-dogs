""" Helper functions for chat """
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday
from django.core.serializers.python import Serializer


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


class PayloadSerializer(Serializer):
    """ Very literal serializing of queryset obj to correct format """

    def get_dump_object(self, qs=None):
        """ Modify default method to create serialized queryset object """
        obj = {}
        obj.update({'message': str(qs.message)})
        obj.update({'user': str(qs.user.username)})
        obj.update({'timestamp': calculate_time(qs.timestamp)})
        obj.update({'pic': str(qs.user.profile_pic.url)})
        obj.update({'id': str(qs.id)})
        return obj
