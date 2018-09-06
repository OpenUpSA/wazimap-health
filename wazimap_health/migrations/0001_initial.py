# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-06 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicHealthFacilities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('settlement', models.CharField(blank=True, max_length=100)),
                ('unit', models.CharField(blank=True, max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=7)),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=7)),
                ('geo_code', models.CharField(max_length=10)),
                ('facility_code', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'db_table': 'public_health_facilities',
            },
        ),
        migrations.CreateModel(
            name='PublicHealthServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oral_pills', models.BooleanField(verbose_name=b'Oral Pills (Contraception)')),
                ('injectables', models.BooleanField()),
                ('iud', models.BooleanField(verbose_name=b'IUDs (Contraception)')),
                ('female_sterialization', models.BooleanField(verbose_name=b'Female Sterilization (Contraception)')),
                ('male_sterialization', models.BooleanField(verbose_name=b'Male Sterilization (Contraception)')),
                ('male_circumcision', models.BooleanField(verbose_name=b'Male Medical Circumcision (MMC)')),
                ('tb', models.BooleanField(verbose_name=b'TB')),
                ('maternal_health', models.BooleanField(verbose_name=b'Maternal Health')),
                ('mental_health', models.BooleanField(verbose_name=b'Mental Health')),
                ('child_health', models.BooleanField(verbose_name=b'Child Health')),
                ('oral_health', models.BooleanField(verbose_name=b'Oral Health Services')),
                ('rehabilitation', models.BooleanField(verbose_name=b'Rehabilitation Services')),
                ('minor_ailments', models.BooleanField(verbose_name=b'Minor Ailments')),
                ('std', models.BooleanField(verbose_name=b'Sexually Transmitted infections Screenings')),
                ('hiv_testing', models.BooleanField(verbose_name=b'HIV Testing')),
                ('hiv_treatment', models.BooleanField(verbose_name=b'HIV Treatment (ART)')),
                ('oral_prep', models.BooleanField(verbose_name=b'Oral PrEP')),
                ('first_trimester', models.BooleanField(verbose_name=b'Termination of Pregnancy - 1st Trimester')),
                ('second_trimester', models.BooleanField(verbose_name=b'Termination of Pregnancy - 2nd Trimester')),
                ('ayfs', models.BooleanField(verbose_name=b'AYFS Accredited')),
                ('ccmdd_pick', models.BooleanField(verbose_name=b'CCMDD Pick Up Point')),
                ('status', models.BooleanField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wazimap_health.PublicHealthFacilities')),
            ],
            options={
                'db_table': 'public_health_services',
            },
        ),
        migrations.AlterUniqueTogether(
            name='publichealthfacilities',
            unique_together=set([('name', 'latitude', 'longitude')]),
        ),
    ]
