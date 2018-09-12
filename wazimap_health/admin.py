from django.contrib import admin

from . import models


class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'facility_type',
                    'latitude', 'longitude', 'ayfs_training', 'geo_code')


admin.site.register(models.PublicHealthFacilities)
admin.site.register(models.PublicHealthServices)
