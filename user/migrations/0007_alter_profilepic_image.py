# Generated by Django 4.1.7 on 2023-10-29 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_pastor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='image',
            field=models.ImageField(upload_to='profile_pic/%y/%m/%d'),
        ),
    ]
