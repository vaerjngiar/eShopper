# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-21 07:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orderitem_product_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='code',
        ),
    ]
