# Generated by Django 2.1.5 on 2019-03-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='private',
            field=models.BooleanField(default=True),
        ),
    ]
