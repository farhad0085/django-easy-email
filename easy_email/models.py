import os

from easy_email.enums import EmailStatus
from . import settings
from django.db import models


def upload_to(instance, filename):
    file_path = os.path.join(settings.EASY_EMAIL_ATTACHMENT_UPLOAD_PATH, filename)
    return file_path


class Attachment(models.Model):
    file = models.FileField(upload_to=upload_to, max_length=500, null=True)


class Email(models.Model):
    """
    Represents an email triggered from the system
    """

    EMAIL_STATUS = [
        [EmailStatus.SUCCESS, "Success"],
        [EmailStatus.ERROR, "Error"],
    ]

    subject = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    recipients = models.TextField(null=True, blank=True)
    from_email = models.CharField(max_length=100, null=True, blank=True)
    cc = models.TextField(null=True, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    send_time = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    status = models.IntegerField(choices=EMAIL_STATUS, null=True, blank=True)
    logs = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

