# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-17 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0016_healthfacilities_parent_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthfacilities',
            name='dataset',
            field=models.CharField(max_length=100),
        ),
    ]
