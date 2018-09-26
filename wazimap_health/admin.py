import csv

from django.contrib import admin
from django.contrib.admin import AdminSite
from django import forms
from django_admin_hstore_widget.forms import HStoreFormField
from django.http import HttpResponse
from wazimap.models import Geography
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
    list_display = ('name', 'settlement', 'unit', 'facility_code', 'dataset',
                    'latitude', 'longitude')
    list_filter = ('dataset', )
    form = HealthFacilityAdminForm
    actions = ['export_csv']

    def _get_fields(self, obj):
        """
        We need to get the fields especially from the service column
        """
        facility_fields = self._flattern(obj, '__').keys()
        sorted_fields = sorted(facility_fields)
        return sorted_fields

    def _flattern(self, obj, separator):
        """
        Convert the dictionary with nested dictionaries to flat dictionary
        """
        facility = {}
        for i in obj.keys():
            if isinstance(obj[i], dict):
                service = flattern(obj[i], separator)
                for j in service.keys():
                    facility[i + separator + j] = service[j]
            else:
                facility[i] = obj[i]
        return facility

    def export_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'

        facility = queryset.values('name', 'address', 'latitude', 'longitude',
                                   'settlement', 'unit', 'service')[0]
        writer = csv.DictWriter(
            response, fieldnames=self._get_fields(facility))
        writer.writeheader()
        for obj in queryset.values('name', 'address', 'latitude', 'longitude',
                                   'settlement', 'unit', 'service'):
            q = self._flattern(obj, '__')
            writer.writerow({
                k: v.encode('utf8') if isinstance(v, unicode) else v
                for k, v in q.items()
            })

        return response

    export_csv.short_description = 'Export Health Facilities'


class HigherEducationAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.HigherEducation
        exclude = ()


class HigherEducationAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'classification', 'facility_code')
    list_filter = ('classification', )
    form = HigherEducationAdminForm


class BasicEducationAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.BasicEducation
        exclude = ()


class BasicEducationAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'phase', 'facility_code')
    list_filter = ('phase', 'sector', 'special_need')
    form = BasicEducationAdminForm


admin_site.register(models.HealthFacilities, HealthFacilityAdmin)
admin_site.register(models.HigherEducation, HigherEducationAdmin)
admin_site.register(Geography)
admin_site.register(models.BasicEducation, BasicEducationAdmin)


def flattern(obj, separator):
    """
    Convert the dictionary with nested dictionaries to flat dictionary
    """
    facility = {}
    for i in obj.keys():
        if isinstance(obj[i], dict):
            service = flattern(obj[i], separator)
            for j in service.keys():
                facility[i + separator + j] = service[j]
        else:
            facility[i] = obj[i]
    return facility
