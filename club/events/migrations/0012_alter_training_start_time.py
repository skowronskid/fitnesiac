# Generated by Django 3.2.5 on 2022-12-31 13:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_training_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 31, 11, 32, 28, 895781, tzinfo=utc)),
        ),
    ]
