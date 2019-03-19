# Generated by Django 2.1.5 on 2019-03-18 02:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20190316_0232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='date_created',
            new_name='published',
        ),
        migrations.RemoveField(
            model_name='post',
            name='privacy',
        ),
        migrations.AddField(
            model_name='post',
            name='contentType',
            field=models.CharField(choices=[('Plain Text', 'text/plain'), ('Markdown', 'text/markdown')], default='Plain Text', max_length=100),
        ),
        migrations.AddField(
            model_name='post',
            name='unlisted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('Private', 'PRIVATE'), ('All friends on my host', 'SERVERONLY'), ('All friends', 'FRIENDS'), ('My friends friends', 'FOAF'), ('Public', 'PUBLIC')], default='Private', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]