# Generated by Django 3.2 on 2025-03-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easy_email', '0005_auto_20250316_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='email',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='template',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
