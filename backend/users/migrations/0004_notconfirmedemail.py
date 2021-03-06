# Generated by Django 4.0 on 2022-01-17 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_is_email_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotConfirmedEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, verbose_name='email that user not confirmed')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
