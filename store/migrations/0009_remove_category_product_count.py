# Generated by Django 3.2.20 on 2023-10-19 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_category_product_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='product_count',
        ),
    ]
