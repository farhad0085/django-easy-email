# Django Easy Email
A Django extension designed to streamline email management with powerful templates, scheduling, storage, and more.

## Features
- Email based OTP authentication
- Email scheduling
- Ability to store email template in database level
- Email sending logs
- Works with any third party storage backend

## Documentation
- [Installation](https://django-easy-email.readthedocs.io/en/latest/installation/)
- [Configuration](https://django-easy-email.readthedocs.io/en/latest/configuration/)
- [Usage](https://django-easy-email.readthedocs.io/en/latest/usage/)
- [Customization](https://django-easy-email.readthedocs.io/en/latest/customization/)
- [Settings](https://django-easy-email.readthedocs.io/en/latest/settings/)
- [API Reference](https://django-easy-email.readthedocs.io/en/latest/api_reference/)

## Important!
### Windows Users
In windows, to run celery, you should use `gevent` along with celery otherwise celery tasks will not evaluate.

- Use following command to install `gevent`
```sh
pip install gevent
```

- Then to run celery worker, run following:
```sh
celery -A project_name worker -l info -P gevent
```
