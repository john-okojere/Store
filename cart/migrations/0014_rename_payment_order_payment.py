# Generated by Django 4.1.7 on 2024-04-06 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Payment',
            new_name='payment',
        ),
    ]
