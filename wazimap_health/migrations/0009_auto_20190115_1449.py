# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-01-15 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0008_auto_20190115_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerlocation',
            name='location_code',
            field=models.CharField(max_length=100),
        ),
    ]
