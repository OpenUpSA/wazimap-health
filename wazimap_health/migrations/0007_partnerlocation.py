# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-01-15 12:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0006_highereducation_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_code', models.CharField(max_length=20)),
                ('location_name', models.CharField(max_length=20)),
                ('activity_number', models.CharField(max_length=2)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='wazimap_health.Organisation')),
            ],
            options={
                'db_table': 'partner_location',
                'verbose_name_plural': 'Partner Locations',
            },
        ),
    ]
