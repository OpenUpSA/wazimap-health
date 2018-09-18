from django.contrib import admin
from django.contrib.admin import AdminSite
from django import forms
from django_admin_hstore_widget.forms import HStoreFormField

from . import models


class HealthAdminSite(AdminSite):
    site_title = 'Clinton Health Access Initiative'
    site_header = 'CHAI Administration'
    index_title = 'CHAI Admin'


admin_site = HealthAdminSite()


class HealthFacilityAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.HealthFacilities
        exclude = ()


class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'settlement', 'unit', 'facility_code',
                    'dataset',
                    'latitude', 'longitude')
    list_filter = ('dataset',)
    form = HealthFacilityAdminForm


admin_site.register(models.HealthFacilities, HealthFacilityAdmin)
