# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-13 14:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20161013_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='products.Product')),
            ],
        ),
    ]
