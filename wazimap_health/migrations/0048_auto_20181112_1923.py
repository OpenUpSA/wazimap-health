# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-12 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0047_auto_20181112_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaimplementation',
            name='activity_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='target',
            name='activity_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partnerhealth',
            name='activity_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='partnerhighereducation',
            name='activity_number',
            field=models.IntegerField(default=0),
        ),
    ]
