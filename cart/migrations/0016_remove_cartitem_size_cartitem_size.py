# Generated by Django 4.1.7 on 2024-04-06 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0006_sizes_remove_product_size_product_size'),
        ('cart', '0015_cartitem_info_cartitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='size',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.ManyToManyField(to='shelf.sizes'),
        ),
    ]
