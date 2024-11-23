from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured


EASY_EMAIL_ATTACHMENT_UPLOAD_PATH = getattr(django_settings, 'EASY_EMAIL_ATTACHMENT_UPLOAD_PATH', 'easy_email/attachments')


if type(EASY_EMAIL_ATTACHMENT_UPLOAD_PATH) != str:
    raise ImproperlyConfigured("EASY_EMAIL_ATTACHMENT_UPLOAD_PATH must be str type")
