# Generated by Django 4.1.7 on 2024-04-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0005_alter_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='shelf.sizes'),
        ),
    ]