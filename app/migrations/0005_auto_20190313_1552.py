# Generated by Django 2.1.5 on 2019-03-13 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_image_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='private',
            field=models.IntegerField(default=0),
        ),
    ]