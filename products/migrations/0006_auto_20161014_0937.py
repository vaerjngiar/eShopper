# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-14 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='photo',
            new_name='photo1',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price_in_dollars',
            new_name='price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price_in_euros',
            new_name='sale_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price_in_pounds',
        ),
        migrations.AddField(
            model_name='product',
            name='photo2',
            field=models.ImageField(blank=True, upload_to='product_photo'),
        ),
    ]
