import os
import filetype
import traceback
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from easy_email.enums import EmailStatus
from easy_email.models import Attachment, Email


class BaseEmailProcessor:
    def __init__(self, subject, email_body, recipient_list, from_email=None, fail_silently=True, **kwargs):
        self.subject = subject
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.message = email_body
        self.html_message = email_body
        self.kwargs = kwargs
        self.process_email()
    
    def get_connection(self):
        connection_data = self.get_connection_data()
        return get_connection(**connection_data)

    def process_email(self):
        connection = self.get_connection()

        # pop files first, files is a list of file objects
        attachment_files = self.kwargs.pop("files", []) or []

        email_obj = self.save_record(attachments=attachment_files)
        
        try:
            msg = EmailMultiAlternatives(
                subject=self.subject,
                body=self.message,
                from_email=self.from_email or self.get_default_from_email(),
                to=self.recipient_list,
                connection=connection,
                **self.kwargs
            )
            msg.attach_alternative(self.html_message, "text/html")
            # attach the files.
            for file in attachment_files:
                msg.attach(
                    filename=os.path.basename(file.name),
                    content=file.read(),
                    mimetype=filetype.guess_mime(file.read()),
                )
            msg.send(self.fail_silently)

            # update email status
            email_obj.is_sent = True
            email_obj.status = EmailStatus.SUCCESS
            email_obj.save()
        except Exception as e:
            email_obj.is_sent = False
            email_obj.status = EmailStatus.ERROR
            email_obj.logs = "".join(traceback.format_exception(None, e, e.__traceback__))
            email_obj.save()


    def get_connection_data(self):
        connection_data = {
            "host": settings.EMAIL_HOST,
            "port": settings.EMAIL_PORT,
            "username": settings.EMAIL_HOST_USER,
            "password": settings.EMAIL_HOST_PASSWORD,
            "use_tls": settings.EMAIL_USE_TLS,
        }
        return connection_data

    def get_default_from_email(self):
        return settings.DEFAULT_FROM_EMAIL

    def save_record(self, attachments):
        # save the mail
        attachment_objs = []
        for file in attachments:
            attachment_objs.append(Attachment.objects.create(file=file))
        
        email_obj = Email.objects.create(
            subject=self.subject,
            body=self.message,
            recipients=self.recipient_list,
            from_email=self.from_email or self.get_default_from_email(),
            cc=self.kwargs.get('cc'),
        )
        
        email_obj.send_time = timezone.now()
        email_obj.attachments.set(attachment_objs)
        email_obj.save()
        return email_obj


class EmailProcessor(BaseEmailProcessor):
    pass

