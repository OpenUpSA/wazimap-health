# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-01 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0044_auto_20181101_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highereducation',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='highereducation',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]