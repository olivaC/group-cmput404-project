# Generated by Django 2.1.5 on 2019-03-26 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='private',
        ),
    ]
