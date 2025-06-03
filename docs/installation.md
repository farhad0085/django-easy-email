# Installation

To get started with Django Easy Email, follow these simple steps to install and configure it in your project:

1. Install the package
```sh
pip install django-easy-email
```

2. Add `easy_email` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'easy_email',
    ...
]
```

3. Modify `TEMPLATES` settings to add loaders.
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'APP_DIRS': True, # important
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # add loaders
            "loaders": [
                "easy_email.loaders.db_template_loader.DatabaseTemplateLoader",
                "django.template.loaders.app_directories.Loader",
                "django.template.loaders.filesystem.Loader",
            ]
        },
    },
]
```

4. Apply database migrations:
```sh
python manage.py migrate
```

5. Learn how to use `Django Easy Email` effectively in the [Usage Guide](./usage.md)


> For a comprehensive list of all available settings options, please refer to the [Settings Documentation](./settings.md)
