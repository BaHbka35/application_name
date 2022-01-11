# Generated by Django 4.0 on 2022-01-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_training_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is user active or his account was deleted?'),
        ),
    ]