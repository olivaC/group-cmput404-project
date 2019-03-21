# Generated by Django 2.1.5 on 2019-03-21 16:25

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('host_url', models.URLField(blank=True, null=True)),
                ('github_url', models.CharField(blank=True, max_length=100, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(blank=True, upload_to='profile_pics')),
                ('friends', models.ManyToManyField(blank=True, related_name='_author_friends_+', to='app.Author')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('comment', models.TextField(default='')),
                ('contentType', models.CharField(choices=[('text/plain', 'Plain Text'), ('text/markdown', 'Markdown')], default='Plain Text', max_length=100)),
                ('published', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorComment', to='app.Author')),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acknowledged', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_request', to='app.Author')),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_request', to='app.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private', models.IntegerField(default=0)),
                ('file', models.FileField(upload_to=app.models.Image.get_image_dir)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorImage', to='app.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('published', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('visibility', models.CharField(choices=[('PRIVATE', 'Private'), ('SERVERONLY', 'All friends on my host'), ('FRIENDS', 'All friends'), ('FOAF', 'My friends friends'), ('PUBLIC', 'Public')], default='Private', max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(default='')),
                ('contentType', models.CharField(choices=[('text/plain', 'Plain Text'), ('text/markdown', 'Markdown')], default='Plain Text', max_length=100)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorPost', to='app.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CommentPost', to='app.Post'),
        ),
    ]
