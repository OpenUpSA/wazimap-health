# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-12-11 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0002_auto_20181130_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partnerbasiceducation',
            options={
                'verbose_name_plural': 'Partner Basic Education Facilities'
            },
        ),
        migrations.AlterModelOptions(
            name='partnerhealth',
            options={'verbose_name_plural': 'Partner Health Facilities'},
        ),
        migrations.AlterModelOptions(
            name='partnerhighereducation',
            options={
                'verbose_name_plural': 'Partner Higher Education Facilities'
            },
        ),
        migrations.AddField(
            model_name='highereducation',
            name='main_campus',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='activity',
            name='hiv_aids_focus',
            field=models.BooleanField(
                default=False, verbose_name='Main Focus on HIV/AIDS'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='highereducation',
            unique_together=set([('name', 'latitude', 'longitude')]),
        ),
    ]
