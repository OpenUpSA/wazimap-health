# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify


class Partner(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='uploads/')
    slug = models.SlugField(
        null=True, blank=True, allow_unicode=True, max_length=255)

    class Meta:
        db_table = 'partner'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Partner, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contact(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'partner_contact'
        unique_together = ('partner', 'name')

    def __str__(self):
        return self.name


class Activity(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='activities')
    activity_number = models.IntegerField()
    hiv_aids_focus = models.BooleanField(
        verbose_name='Main Focus on HIV/AIDS', default=False)
    category = models.CharField(
        max_length=100,
        verbose_name='Implementation activity category',
        blank=True,
        null=True)
    other_category = models.TextField(blank=True, null=True)
    donor_agency = models.TextField(blank=True, null=True)
    activity = models.TextField(blank=True, null=True)
    she_conquers_element = models.CharField(
        max_length=100, blank=True, null=True)
    other_she_conquers = models.CharField(
        max_length=255, blank=True, null=True)
    timeline = models.CharField(max_length=100, blank=True, null=True)
    audience = models.CharField(max_length=255, blank=True, null=True)
    other_audience = models.TextField(blank=True, null=True)
    location_type = models.TextField(blank=True, null=True)
    other_location_type = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    more_province = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    municipality = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'partner_activity'

    def __str__(self):
        return self.activity


class HigherEducationFacility(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='higher_ed')
    province = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)
    campus = models.CharField(max_length=100)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_higher_education_facility'
        verbose_name_plural = 'Partner Higher Education Facility'

    def __str__(self):
        return self.institution


class HealthFacility(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='health')
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    facility = models.CharField(max_length=50)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_health_facility'
        verbose_name_plural = 'Partner Health Facility'

    def __str__(self):
        return self.facility


class BasicEducationFacility(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='basic_ed')
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_basic_education_facility'
        verbose_name_plural = 'Partner Basic Education Facility'

    def __str__(self):
        return self.school


class Location(models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name='location')
    location_code = models.CharField(max_length=10)
    location_name = models.CharField(max_length=100)
    activity_number = models.IntegerField(default=0)

    class Meta:
        db_table = 'partner_location'
        verbose_name_plural = 'Partner Location'

    def __str__(self):
        return self.location_name
