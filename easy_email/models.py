import os
from easy_email.enums import EmailStatus
from easy_email.validators import TemplateNameValidator
from easy_email.settings import settings
from django.db import models


def upload_to(instance, filename):
    file_path = os.path.join(settings.EASY_EMAIL_ATTACHMENT_UPLOAD_PATH, filename)
    return file_path

def storage_backend():
    return settings.EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND


class Attachment(models.Model):
    file = models.FileField(upload_to=upload_to, max_length=500, null=True, storage=storage_backend)

    def __str__(self):
        return self.file.name if self.file else f"File ID - {self.id}"


class Email(models.Model):
    """
    Represents an email triggered from the system
    """

    EMAIL_STATUS = [
        [EmailStatus.PENDING, "Pending"],
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
    status = models.IntegerField(choices=EMAIL_STATUS, default=EmailStatus.PENDING, null=True, blank=True)
    logs = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.subject or f"Email ID - {self.id}"


class Template(models.Model):
    name = models.CharField(max_length=50, validators=[TemplateNameValidator()], unique=True,
        help_text="Only underscore (_), lowercase characters, and numbers are allowed. Name cannot start with a number.")
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name or f"Template ID - {self.id}"
