# Generated by Django 2.1.5 on 2019-04-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_post_visibleto'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='no_images',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='server',
            name='no_posts',
            field=models.BooleanField(default=False),
        ),
    ]