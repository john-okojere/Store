# Generated by Django 4.1.7 on 2024-04-13 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0006_sizes_remove_product_size_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delivery',
            field=models.CharField(choices=[('Free Delivery', 'Free Delivery'), ('Delivery Fee', 'Delivery Fee')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='pay',
            field=models.CharField(choices=[('Pay on Delivery', 'Pay on Delivery'), ('Pay before Delivery', 'Pay before Delivery')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='productType',
            field=models.CharField(choices=[('Single Buy', 'Single Buy'), ('Min. Buy', 'Min. Buy'), ('Gift on Buy', 'Gift on Buy')], max_length=25, null=True),
        ),
    ]