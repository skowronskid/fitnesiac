# Generated by Django 3.2.5 on 2023-01-05 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20230105_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 5, 18, 24, 20, 97033)),
        ),
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 5, 16, 54, 20, 97016)),
        ),
    ]
