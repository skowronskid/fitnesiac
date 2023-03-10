# Generated by Django 3.2.5 on 2023-01-06 15:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('events', '0001_initial'), ('events', '0002_auto_20221230_1722'), ('events', '0003_auto_20221230_1756'), ('events', '0004_auto_20221231_1136'), ('events', '0005_auto_20221231_1154'), ('events', '0006_auto_20221231_1201'), ('events', '0007_auto_20221231_1210'), ('events', '0008_alter_training_start_time'), ('events', '0009_alter_training_start_time'), ('events', '0010_alter_training_start_time'), ('events', '0011_alter_training_start_time'), ('events', '0012_alter_training_start_time'), ('events', '0013_auto_20230102_1234'), ('events', '0014_auto_20230102_1327'), ('events', '0015_auto_20230102_1336'), ('events', '0016_auto_20230102_1347'), ('events', '0017_alter_training_start_time'), ('events', '0018_alter_training_start_time'), ('events', '0019_alter_training_start_time'), ('events', '0020_training_description_alter_training_end_time_and_more'), ('events', '0021_rename_description_training_describtion_and_more'), ('events', '0022_auto_20230105_1620'), ('events', '0023_auto_20230105_1720'), ('events', '0024_auto_20230105_1753'), ('events', '0025_auto_20230105_1800'), ('events', '0026_auto_20230105_1824'), ('events', '0027_auto_20230105_1828'), ('events', '0028_auto_20230105_1829'), ('events', '0029_auto_20230105_2201'), ('events', '0030_alter_training_end_time_alter_training_start_time')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True, verbose_name='Target')),
                ('bodyPart', models.CharField(blank=True, max_length=120, null=True, verbose_name='Body Part')),
                ('equipment', models.CharField(blank=True, max_length=120, null=True, verbose_name='Equipment')),
                ('gifUrl', models.CharField(blank=True, max_length=500, null=True, verbose_name='Gif URL')),
                ('target', models.CharField(blank=True, max_length=300, null=True, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Training name')),
                ('date', models.DateField()),
                ('start_time', models.TimeField(default=datetime.datetime(2023, 1, 6, 9, 35, 39, 765084))),
                ('end_time', models.TimeField(default=datetime.datetime(2023, 1, 6, 11, 5, 39, 765084))),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('date_created', models.DateTimeField(auto_created=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sets', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], verbose_name='Number of sets')),
                ('reps', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19)], verbose_name='Number of reps in a set')),
                ('exercise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='events.exercise')),
                ('training', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.training')),
                ('weight', models.FloatField(default=0, verbose_name='Weight')),
                ('unit', models.CharField(choices=[('pounds', 'pounds'), ('kilogram', 'kilogram')], default='kilogram', max_length=10)),
            ],
        ),
    ]
