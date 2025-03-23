import traceback
from celery import shared_task
from django.template import Template as TemplateEngine, Context
from django.core.mail import EmailMultiAlternatives, get_connection
import filetype
from easy_email.enums import EmailStatus
from easy_email.exceptions import TemplateNotFound
from easy_email.models import Attachment, Email, Template


def render_email_template(template_name, context=None, request=None):
    try:
        template = Template.objects.get(name=template_name)
    except:
        raise TemplateNotFound(template_name)
    
    template_engine = TemplateEngine(template_string=template.content)
    context = Context({'request': request, **context })
    email_content = template_engine.render(context)
    return email_content


@shared_task
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

