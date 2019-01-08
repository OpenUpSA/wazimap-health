# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-12-11 14:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0003_auto_20181211_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='highereducation',
            name='institution',
        ),
        migrations.AlterUniqueTogether(
            name='highereducation',
            unique_together=set([('name', 'latitude', 'longitude', 'facility_code')]),
        ),
    ]