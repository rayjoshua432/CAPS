# Generated by Django 3.2.20 on 2023-10-21 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_category_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='products',
        ),
    ]
