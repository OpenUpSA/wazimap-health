# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-06 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publichealthfacilities',
            old_name='geo_code',
            new_name='parent_geo_code',
        ),
    ]
