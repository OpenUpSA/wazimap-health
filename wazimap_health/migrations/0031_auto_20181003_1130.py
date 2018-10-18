# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-10-03 09:30
from __future__ import unicode_literals

from django.db import migrations


def delete_wards(apps, schema_editor):
    Geography = apps.get_model('wazimap', 'Geography')
    for ward in Geography.objects.filter(geo_level='ward'):
        ward.delete()


class Migration(migrations.Migration):

    dependencies = [('wazimap_health',
                     '0030_remove_healthfacilities_parent_name'),
                    ('wazimap', '0008_auto_20170424_1209')]

    operations = [migrations.RunPython(delete_wards)]