# Generated by Django 3.2.5 on 2022-12-31 12:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20221231_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Target'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='target',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 31, 10, 40, 21, 117994, tzinfo=utc)),
        ),
    ]
