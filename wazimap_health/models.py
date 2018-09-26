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
    parent_name = models.CharField(max_length=100, blank=True)
    dataset = models.CharField(max_length=20)
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
