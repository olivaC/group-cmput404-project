# Generated by Django 2.1.5 on 2019-03-15 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20190313_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(to='app.Author'),
        ),
    ]