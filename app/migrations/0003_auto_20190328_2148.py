# Generated by Django 2.1.5 on 2019-03-28 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20190328_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='hostname',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='server',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
