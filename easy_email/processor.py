import filetype
import traceback
from typing import List
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection
from easy_email.enums import EmailStatus
from easy_email.exceptions import InvalidFileFormat, InvalidSendTime
from easy_email.models import Attachment, Email
from typing import Optional, Union


class BaseEmailProcessor:
    def __init__(self, subject, email_body, recipient_list,
            from_email=None, fail_silently=True, **kwargs):
        """
        Initializes the email processor with the given email details and optional parameters.

        Args:
        - subject (str): The subject of the email.
        - email_body (str): The body content of the email (plain text).
        - recipient_list (list): A list of email addresses to which the email will be sent.
        - from_email (str, optional): The sender's email address. If not provided, a default will be used.
        - fail_silently (bool, optional): A flag that determines whether to suppress exceptions if an error occurs during email sending. Default is True (suppress errors).
        
        Keyword Arguments (kwargs):
        - files (list, optional): A list of `Attachment` objects that will be included with the email. The list is passed via `kwargs`.

        Attributes:
        - subject (str): The email subject.
        - recipient_list (list): The list of recipients for the email.
        - from_email (str): The sender's email address.
        - fail_silently (bool): Whether to fail silently or raise errors when sending the email.
        - message (str): The plain text body of the email.
        - html_message (str): The HTML body of the email (same as `message` in this case).
        - send_time (datetime, optional): The time at which the email should be sent. Defaults to None (send immediately).
        """
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

    def _process_files(self) -> List[Attachment]:
        """
        This method processes the 'files' parameter from kwargs, ensuring that all
        files provided are instances of the Attachment class. It returns a list of valid 
        Attachment objects after performing the check.

        Input:
        - No explicit input, uses the `files` keyword argument passed to the class.

        Output:
        - List of `Attachment` objects (valid files). If any of the files are not 
        `Attachment` objects, an exception is raised.

        Raises:
        - InvalidFileFormat: If any item in the `files` list is not an instance of the 
        `Attachment` class.
        """
        # Extract the "files" from kwargs, default to an empty list if not provided
        attachments = self.kwargs.pop("files", []) or []

        # Check that all items in attachments are instances of Attachment
        for attachment in attachments:
            if not isinstance(attachment, Attachment):
                # Raise an error if the file is not an instance of the Attachment class
                raise InvalidFileFormat("All files must be instances of the Attachment class")
        
        # Return the list of valid Attachment objects
        return attachments

    def _process_email(self):
        connection = self.get_connection()

        attachments = self._process_files()
        email_obj = self._save_email()
        
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
            for attachment in attachments:
                msg.attach(
                    filename=attachment.file.name,
                    content=attachment.file.read(),
                    mimetype=filetype.guess_mime(attachment.file.read()),
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

    def _save_email(self):
        attachment_objs = self._process_files()
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


class CeleryEmailProcessor(BaseEmailProcessor):
    pass
