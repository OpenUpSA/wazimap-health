# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-12 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0049_auto_20181112_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='audience',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='location_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='more_province',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='municipality',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='other_audience',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='other_location_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='province',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]