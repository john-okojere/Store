# Generated by Django 4.1.7 on 2024-03-16 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0004_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
