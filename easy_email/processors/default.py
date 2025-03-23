
from easy_email.exceptions import InvalidEmailProcessor
from easy_email.processors.base import BaseEmailProcessor
from django.utils import timezone


class DefaultEmailProcessor(BaseEmailProcessor):
    
    def get_send_time(self, raw_send_time=None):
        if raw_send_time:
            raise InvalidEmailProcessor("`DefaultEmailProcessor` doesn't support email scheduling, "
                "please use `CeleryEmailProcessor` instead.")
        return timezone.now()

