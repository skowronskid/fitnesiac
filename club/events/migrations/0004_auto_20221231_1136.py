# Generated by Django 3.2.5 on 2022-12-31 11:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20221230_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='body_part',
        ),
        migrations.AddField(
            model_name='exercise',
            name='bodyPart',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Body Part'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='equipment',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Equipment'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='gifUrl',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Gif URL'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='id2',
            field=models.IntegerField(blank=True, null=True, verbose_name='Id2'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='target',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Target'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='training',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2022, 12, 31, 10, 6, 8, 936826, tzinfo=utc)),
        ),
    ]
