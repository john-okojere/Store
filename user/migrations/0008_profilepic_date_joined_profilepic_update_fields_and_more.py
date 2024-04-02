# Generated by Django 4.1.7 on 2023-10-29 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_profilepic_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepic',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='profilepic',
            name='update_fields',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('about', models.TextField()),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_fields', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='aboutprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
