# Generated by Django 4.0 on 2022-02-04 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0003_rename_date_start_challenge_datetime_start'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='datetime_finish',
            new_name='finish_datetime',
        ),
        migrations.RenameField(
            model_name='challenge',
            old_name='datetime_start',
            new_name='start_datetime',
        ),
    ]
