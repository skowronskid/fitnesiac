# Generated by Django 3.2.5 on 2023-01-02 21:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_alter_training_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2023, 1, 2, 20, 29, 45, 807879, tzinfo=utc)),
        ),
    ]
