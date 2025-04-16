# django-easy-email

A Django extension designed to streamline email management with powerful templates, scheduling, storage, and more.

## Windows Users
In windows, to run celery, you should use `gevent` alongside celery otherwise celery tasks are not gonna evaluate.

- Use following command to install `gevent`
```sh
pip install gevent
```

- Then while running celery worker, run following:
```sh
celery -A project_name worker -l info -P gevent
```
