# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-17 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0017_auto_20180917_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthfacilities',
            name='dataset',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='healthfacilities',
            name='parent_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]