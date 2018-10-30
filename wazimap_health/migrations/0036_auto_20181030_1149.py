# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-10-30 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0035_auto_20181030_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activity',
            name='category',
            field=models.CharField(blank=True, max_length=100, verbose_name='Implementation activity category'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='donor_agency',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='other_category',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='other_she_conquers',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='activity',
            name='she_conquers_element',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timeline',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='areaimplementation',
            name='district_municiplaity',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='areaimplementation',
            name='location_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='areaimplementation',
            name='more_province',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='areaimplementation',
            name='other_location_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='areaimplementation',
            name='province',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='target',
            name='audience',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='target',
            name='other_audience',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
