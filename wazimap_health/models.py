from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField


class HealthFacilities(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(decimal_places=5, max_digits=7)
    longitude = models.DecimalField(decimal_places=5, max_digits=7)
    settlement = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    facility_code = models.CharField(max_length=20, unique=True)
    geo_levels = ArrayField(models.CharField(max_length=20), blank=True, null=True)
    parent_name = models.CharField(max_length=100, blank=True)
    dataset = models.CharField(max_length=20)
    service = HStoreField()

    class Meta:
        db_table = 'health_facilities'
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name
