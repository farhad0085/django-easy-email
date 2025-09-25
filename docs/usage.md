# Usage
To integrate `django-easy-email` into your Django project, follow these simple steps:


## Send email immediately

```python
from easy_email.utils import render_email_template
from easy_email.processors.default import DefaultEmailProcessor


subject = "Test Email"
context = {}
body = render_email_template('path/to/email_template.html', context)
recipients = ['email1@gmail.com', 'email2@yahoo.com']

email = DefaultEmailProcessor(
    subject=subject,
    email_body=body,
    recipient_list=recipients,
)
email.send()
```

## Schedule Email

To schedule an email, you have to use `CeleryEmailProcessor` from `easy_email.processors.celery` package. An example might be as following:


```python
from datetime import timedelta
from easy_email.utils import render_email_template
from easy_email.processors.celery import CeleryEmailProcessor


subject = "Test Email"
context = {}
body = render_email_template('path/to/email_template.html', context)
recipients = ['email1@gmail.com', 'email2@yahoo.com']
send_at = timedelta(minutes=10) # supports timedelta, or if int is provided, it'll be treated as seconds

email = CeleryEmailProcessor(
    subject=subject,
    email_body=body,
    recipient_list=recipients,
)
email.send(send_at)
```

## Sending Files

In order to send files in the email, use `Attachment` model to upload the file first. For a clear understanding, follow the example:

```python
from easy_email.utils import render_email_template
from easy_email.processors.default import DefaultEmailProcessor
from easy_email.models import Attachment


subject = "Test Email"
context = {}
body = render_email_template('path/to/email_template.html', context)
recipients = ['email1@gmail.com', 'email2@yahoo.com']

file = ... # some file
attachment = Attachment.objects.create(file=file)

email = DefaultEmailProcessor(
    subject=subject,
    email_body=body,
    recipient_list=recipients,
    files=[attachment]
)
email.send()
```

## Use Email Templates from Database

In order to use email templates from database (useful when you have to create dynamic emails) instead of creating email templates, you'll have to use `render_email_template` utility function available in `easy_email.utils` package. The first argument accept the template name, second one is the template context. Full steps are as follows!

> Note: To use email templates from database, please follow step #3 in [installation page](https://django-easy-email.readthedocs.io/en/latest/installation/#3-modify-templates-settings-to-add-loaders)!

```python
from easy_email.utils import render_email_template
from easy_email.processors.default import DefaultEmailProcessor
from easy_email.models import Attachment


subject = "Test Email"
context = {}
body = render_email_template('email_template_1', context)
recipients = ['email1@gmail.com', 'email2@yahoo.com']

email = DefaultEmailProcessor(
    subject=subject,
    email_body=body,
    recipient_list=recipients,
)
email.send()
```