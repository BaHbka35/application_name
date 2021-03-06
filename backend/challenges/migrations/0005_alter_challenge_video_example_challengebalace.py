# Generated by Django 4.0 on 2022-02-07 16:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_rename_datetime_finish_challenge_finish_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='video_example',
            field=models.FileField(blank=True, null=True, upload_to='video_examples', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name='example of perform'),
        ),
        migrations.CreateModel(
            name='ChallengeBalace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coins_amount', models.PositiveIntegerField(verbose_name='coins amount')),
                ('challenge', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
            ],
        ),
    ]
