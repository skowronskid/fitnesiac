# Generated by Django 3.2.5 on 2023-01-05 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20230105_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 5, 18, 0, 35, 347370)),
        ),
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 5, 16, 30, 35, 347352)),
        ),
    ]
