# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-30 10:50
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_number', models.IntegerField()),
                ('hiv_aids_focus', models.BooleanField(verbose_name='Main Focus on HIV/AIDS')),
                ('category', models.CharField(blank=True, max_length=100, null=True, verbose_name='Implementation activity category')),
                ('other_category', models.CharField(blank=True, max_length=100, null=True)),
                ('donor_agency', models.CharField(blank=True, max_length=100, null=True)),
                ('activity', models.CharField(blank=True, max_length=255, null=True)),
                ('she_conquers_element', models.CharField(blank=True, max_length=100, null=True)),
                ('other_she_conquers', models.CharField(blank=True, max_length=255, null=True)),
                ('timeline', models.CharField(blank=True, max_length=100, null=True)),
                ('audience', models.CharField(blank=True, max_length=255, null=True)),
                ('other_audience', models.CharField(blank=True, max_length=255, null=True)),
                ('location_type', models.CharField(blank=True, max_length=255, null=True)),
                ('other_location_type', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('more_province', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=255, null=True)),
                ('municipality', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'partner_activity',
            },
        ),
        migrations.CreateModel(
            name='AreaImplementation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_type', models.CharField(blank=True, max_length=255, null=True)),
                ('other_location_type', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=100, null=True)),
                ('more_province', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=255, null=True)),
                ('municipality', models.TextField(blank=True, null=True)),
                ('activity_number', models.IntegerField(default=0)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='area_activity', to='wazimap_health.Activity')),
            ],
            options={
                'db_table': 'partner_area_implementation',
            },
        ),
        migrations.CreateModel(
            name='BasicEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(blank=True, max_length=100)),
                ('sector', models.CharField(blank=True, max_length=50)),
                ('phase', models.CharField(blank=True, max_length=20)),
                ('special_need', models.CharField(max_length=5)),
                ('dataset', models.CharField(max_length=50)),
                ('facility_code', models.CharField(max_length=100, unique=True)),
                ('geo_levels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None)),
                ('service', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'basic_education',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'partner_contact',
            },
        ),
        migrations.CreateModel(
            name='HealthFacilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('settlement', models.CharField(blank=True, max_length=100)),
                ('unit', models.CharField(blank=True, max_length=50)),
                ('facility_code', models.CharField(max_length=20, unique=True)),
                ('geo_levels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None)),
                ('dataset', models.CharField(max_length=50)),
                ('service', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'health_facilities',
            },
        ),
        migrations.CreateModel(
            name='HigherEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100, verbose_name='School Name')),
                ('facility_code', models.CharField(max_length=100, unique=True)),
                ('classification', models.CharField(blank=True, max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(blank=True, max_length=100)),
                ('dataset', models.CharField(max_length=20)),
                ('geo_levels', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None)),
                ('service', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
            options={
                'db_table': 'higher_education',
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo', models.ImageField(upload_to='uploads/')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'partner_orgainisation',
            },
        ),
        migrations.CreateModel(
            name='PartnerBasicEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('school', models.CharField(max_length=50)),
                ('activity_number', models.CharField(max_length=10)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basic_ed', to='wazimap_health.Organisation')),
            ],
            options={
                'db_table': 'partner_basic_education_facilities',
            },
        ),
        migrations.CreateModel(
            name='PartnerHealth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('facility', models.CharField(max_length=50)),
                ('activity_number', models.IntegerField(default=0)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health', to='wazimap_health.Organisation')),
            ],
            options={
                'db_table': 'partner_health_facilities',
            },
        ),
        migrations.CreateModel(
            name='PartnerHigherEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=50)),
                ('institution', models.CharField(max_length=50)),
                ('campus', models.CharField(max_length=100)),
                ('activity_number', models.IntegerField(default=0)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='higher_ed', to='wazimap_health.Organisation')),
            ],
            options={
                'db_table': 'partner_higher_education_facilities',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audience', models.CharField(blank=True, max_length=255, null=True)),
                ('other_audience', models.CharField(blank=True, max_length=255, null=True)),
                ('activity_number', models.IntegerField(default=0)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_activity', to='wazimap_health.Activity')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='wazimap_health.Organisation')),
            ],
            options={
                'db_table': 'partner_target',
            },
        ),
        migrations.AlterUniqueTogether(
            name='highereducation',
            unique_together=set([('name', 'latitude', 'longitude', 'institution')]),
        ),
        migrations.AlterUniqueTogether(
            name='healthfacilities',
            unique_together=set([('name', 'latitude', 'longitude', 'facility_code')]),
        ),
        migrations.AddField(
            model_name='contact',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='wazimap_health.Organisation'),
        ),
        migrations.AlterUniqueTogether(
            name='basiceducation',
            unique_together=set([('name', 'latitude', 'longitude')]),
        ),
        migrations.AddField(
            model_name='areaimplementation',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='wazimap_health.Organisation'),
        ),
        migrations.AddField(
            model_name='activity',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='wazimap_health.Organisation'),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('organisation', 'name')]),
        ),
    ]
