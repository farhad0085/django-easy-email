# Generated by Django 2.2 on 2024-11-25 17:46

from django.db import migrations, models
import easy_email.validators


class Migration(migrations.Migration):

    dependencies = [
        ('easy_email', '0002_auto_20241125_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Only underscore (_), lowercase characters, and numbers are allowed. Name cannot start with a number.', max_length=50, validators=[easy_email.validators.TemplateNameValidator()])),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]