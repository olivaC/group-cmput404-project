# Generated by Django 2.1.5 on 2019-03-16 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_author_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_author_friends_+', to='app.Author'),
        ),
    ]