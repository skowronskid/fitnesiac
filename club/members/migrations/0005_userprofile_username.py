# Generated by Django 3.2.5 on 2023-01-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]