# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-18 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20161018_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(blank=True, max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manufacturers', to='products.Product')),
            ],
        ),
    ]
