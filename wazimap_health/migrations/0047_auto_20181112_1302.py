# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-11-12 11:02
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def slugify_programme(apps, schema_editor):
    Organisation = apps.get_model('wazimap_health', 'Organisation')
    for org in Organisation.objects.all():
        org.slug = slugify(org.name)
        org.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wazimap_health', '0046_organisation_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='slug',
            field=models.SlugField(
                null=True, blank=True, max_length=255, allow_unicode=True),
            preserve_default=False,
        ),
        migrations.RunPython(slugify_programme)
    ]