import filetype
import traceback
from celery import current_app
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives, get_connection
from easy_email.enums import EmailStatus
from easy_email.exceptions import InvalidEmailProcessor, InvalidSendTime
from easy_email.processors.base import BaseEmailProcessor
from easy_email.models import Attachment, Email


@current_app.task
def schedule_email(subject, message, from_email, recipient_list, cc, fail_silently, email_id, connection_data, attachment_ids):
    email_obj = Email.objects.get(id=email_id)
    attachments = Attachment.objects.filter(id__in=attachment_ids)
    connection = get_connection(**connection_data)
    
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            connection=connection,
            cc=cc,
        )
        # attach html text
        msg.attach_alternative(message, "text/html")
        # attach the files.
        for attachment in attachments:
            msg.attach(
                filename=attachment.file.name,
                content=attachment.file.read(),
                mimetype=filetype.guess_mime(attachment.file.read()),
            )
        msg.send(fail_silently)

        # update email status
        email_obj.status = EmailStatus.SUCCESS
        email_obj.save()
    except Exception as e:
        email_obj.status = EmailStatus.ERROR
        email_obj.logs = "".join(traceback.format_exception(None, e, e.__traceback__))
        email_obj.save()


class CeleryEmailProcessor(BaseEmailProcessor):
    
    def get_send_time(self, raw_send_time=None):
        if not raw_send_time:
            raise InvalidEmailProcessor("If you don't want to schedule the email, "
                "please use `DefaultEmailProcessor` instead.")
        
        current_time = timezone.now()  # Get the current time with timezone info
        
        # If raw_send_time is a datetime, check if it's in the future
        if isinstance(raw_send_time, timezone.datetime):
            if raw_send_time > current_time:
                # If the send time is in the future, process the email
                return raw_send_time
            else:
                # Raise an exception if the send time is in the past
                raise InvalidSendTime(f"The specified datetime '{raw_send_time}' is in the past")
        
        # If raw_send_time is an integer (in seconds), schedule the email after that delay
        elif isinstance(raw_send_time, int):
            # Schedule the email by adding seconds to the current time
            return current_time + timedelta(seconds=raw_send_time)

        else:
            # Raise an exception for invalid send_time type
            raise InvalidSendTime()

    def send(self, send_time):
        send_time = self.get_send_time(send_time)
        email_obj = self._save_email(send_time)
        # set email status to Pending initially
        email_obj.status = EmailStatus.PENDING
        email_obj.save()
        connection_data = self.get_connection_data()

        # no way to call a class method using .apply_async() or .delay()
        # so creating a function outside the class to handle the scheduling
        schedule_email.apply_async((
            self.subject,
            self.message,
            self.from_email or self.get_default_from_email(),
            self.recipient_list,
            self.kwargs.get('cc'),
            self.fail_silently,
            email_obj.id,
            connection_data,
            [att.id for att in self._process_files()]
        ), eta=send_time)
