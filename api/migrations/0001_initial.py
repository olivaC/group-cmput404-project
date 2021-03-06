# Generated by Django 2.1.5 on 2019-04-01 06:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0004_auto_20190329_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foreignServer', to='app.Server')),
            ],
        ),
    ]
