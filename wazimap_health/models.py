from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField


class HealthFacilities(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    settlement = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    facility_code = models.CharField(max_length=20, unique=True)
    geo_levels = ArrayField(
        models.CharField(max_length=20), blank=True, null=True)
    dataset = models.CharField(max_length=50)
    service = HStoreField()

    class Meta:
        db_table = 'health_facilities'
        unique_together = ('name', 'latitude', 'longitude', 'facility_code')

    def __str__(self):
        return self.name


class HigherEducation(models.Model):
    institution = models.CharField(max_length=100)
    name = models.CharField(max_length=100, verbose_name='School Name')
    facility_code = models.CharField(max_length=100, unique=True)
    classification = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100, blank=True)
    dataset = models.CharField(max_length=20)
    geo_levels = ArrayField(
        models.CharField(max_length=20), blank=True, null=True)
    service = HStoreField()

    class Meta:
        db_table = 'higher_education'
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name


class BasicEducation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=50, blank=True)
    phase = models.CharField(max_length=20, blank=True)
    special_need = models.CharField(max_length=5)
    dataset = models.CharField(max_length=50)
    facility_code = models.CharField(max_length=100, unique=True)
    geo_levels = ArrayField(
        models.CharField(max_length=20), blank=True, null=True)
    service = HStoreField()

    class Meta:
        db_table = 'basic_education'
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name


class Organisation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='uploads/')

    class Meta:
        db_table = 'partner_orgainisation'

    def __str__(self):
        return self.name


class Contact(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'partner_contact'
        unique_together = ('organisation', 'name')


class Activity(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='activities')
    activity_number = models.IntegerField()
    hiv_aids_focus = models.BooleanField(verbose_name='Main Focus on HIV/AIDS')
    category = models.CharField(
        max_length=100, verbose_name='Implementation activity category')
    other_category = models.CharField(max_length=100)
    donor_agency = models.CharField(max_length=100)
    activity = models.CharField(max_length=255)
    she_conquers_element = models.CharField(max_length=100)
    other_she_conquers = models.CharField(max_length=255)
    timeline = models.CharField(max_length=100)

    class Meta:
        db_table = 'partner_activity'


class Target(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='targets')
    audience = models.CharField(max_length=255)
    other_audience = models.CharField(max_length=255)

    class Meta:
        db_table = 'partner_target'


class AreaImplementation(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name='areas')
    location_type = models.CharField(max_length=255)
    other_location_type = models.CharField(max_length=255)
    province = models.CharField(max_length=20)
    more_province = models.CharField(max_length=20)
    district_municiplaity = models.CharField(max_length=100)


class Meta:
    db_table = 'partner_area_implementation'
