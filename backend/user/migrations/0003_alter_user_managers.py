# Generated by Django 4.1.1 on 2022-09-17 21:31

from django.db import migrations
import user.managers


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_user_title'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user.managers.CustomUserManager()),
            ],
        ),
    ]
