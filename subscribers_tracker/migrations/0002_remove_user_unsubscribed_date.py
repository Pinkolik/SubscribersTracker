# Generated by Django 2.1.7 on 2019-05-27 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='unsubscribed_date',
        ),
    ]
