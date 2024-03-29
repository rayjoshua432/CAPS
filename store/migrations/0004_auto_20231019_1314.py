# Generated by Django 3.2.20 on 2023-10-19 05:14

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='icons/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
