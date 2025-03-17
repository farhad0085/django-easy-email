from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.core.files.storage import default_storage


class EasyEmailSettings:
    # settings variables
    EASY_EMAIL_ATTACHMENT_UPLOAD_PATH = None
    EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND = None

    # set _instance to None initially
    _instance = None

    def __new__(cls, *args, **kwargs):
        # follow singleton design pattern, so that only one setting instance is created
        if not cls._instance:
            cls._instance = super(EasyEmailSettings, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_settings()
        return cls._instance

    def _initialize_settings(self):
        self._validate_and_set_attachments_path()
        self._validate_and_set_storage_backend()

    def _validate_and_set_attachments_path(self):
        self.EASY_EMAIL_ATTACHMENT_UPLOAD_PATH = getattr(django_settings, 'EASY_EMAIL_ATTACHMENT_UPLOAD_PATH', 'easy_email/attachments')
        if type(self.EASY_EMAIL_ATTACHMENT_UPLOAD_PATH) != str:
            raise ImproperlyConfigured("EASY_EMAIL_ATTACHMENT_UPLOAD_PATH must be str type")

    def _validate_and_set_storage_backend(self):
        storage_backend = getattr(django_settings, 'EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND', None)
        if storage_backend:
            if type(storage_backend) != str:
                raise ImproperlyConfigured("EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND must be str type")
            # Attempt to import the storage backend if it's provided
            try:
                self.EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND = import_string(storage_backend)()
            except (ImportError, AttributeError) as e:
                raise ImproperlyConfigured(f"Could not import storage backend '{storage_backend}': {e}")
        else:
            self.EASY_EMAIL_ATTACHMENT_STORAGE_BACKEND = default_storage

settings = EasyEmailSettings()
