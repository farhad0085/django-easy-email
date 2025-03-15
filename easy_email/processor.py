import os
import filetype
import traceback
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from easy_email.enums import EmailStatus
from easy_email.exceptions import InvalidSendTime
from easy_email.models import Attachment, Email
from typing import Optional, Union

class BaseEmailProcessor:
    def __init__(self, subject, email_body, recipient_list,
            from_email=None, fail_silently=True, **kwargs):
        self.subject = subject
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.message = email_body
        self.html_message = email_body
        self.send_time = None
        self.kwargs = kwargs
    
    def get_connection(self):
        connection_data = self.get_connection_data()
        return get_connection(**connection_data)
    
    def send(self, send_time: Optional[Union[None, timezone.datetime, int]]=None):
        """
        Arguments:
        - send_time (Optional[Union[None, datetime, int]]): Determines when to send the email.
            - None: Sends the email instantly.
            - datetime: Sends the email at the specified future datetime.
            - int: Sends the email after the specified number of seconds (delay).
            
        If the datetime is in the past, the function will raise an error. If an integer is provided, it will be interpreted as a delay in seconds, and the email will be sent after that duration.
        """

        current_time = timezone.now()  # Get the current time with timezone info

        # If send_time is None, send the email instantly
        if send_time is None:
            self.send_time = current_time
            self._process_email()
        
        # If send_time is a datetime, check if it's in the future
        elif isinstance(send_time, timezone.datetime):
            if send_time > current_time:
                # If the send time is in the future, process the email
                self.send_time = send_time
                self._process_email()
            else:
                # Raise an exception if the send time is in the past
                raise InvalidSendTime(send_time)
        
        # If send_time is an integer (in seconds), schedule the email after that delay
        elif isinstance(send_time, int):
            # Schedule the email by adding seconds to the current time
            self.send_time = current_time + timedelta(seconds=send_time)
            self._process_email()

        else:
            # Raise an exception for invalid send_time type
            raise InvalidSendTime(send_time)

    def _process_email(self):
        connection = self.get_connection()

        # pop files first, files is a list of file objects
        attachment_files = self.kwargs.pop("files", []) or []

        email_obj = self._save_email(attachments=attachment_files)
        
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
            email_obj.status = EmailStatus.SUCCESS
            email_obj.save()
        except Exception as e:
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

    def _save_email(self, attachments):
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
        
        email_obj.send_time = self.send_time
        email_obj.attachments.set(attachment_objs)
        email_obj.save()
        return email_obj


class DefaultEmailProcessor(BaseEmailProcessor):
    pass


class RedisEmailProcessor(BaseEmailProcessor):
    pass
