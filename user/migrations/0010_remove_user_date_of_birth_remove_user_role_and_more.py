# Generated by Django 4.1.7 on 2024-03-17 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_delete_pastor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
