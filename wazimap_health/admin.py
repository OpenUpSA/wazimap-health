import csv
import xlwt

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

    def export_csv(self, request, queryset):
        field_names = [
            'facility_code', 'name', 'latitude', 'longitude', 'address',
            'settlement', 'unit'
        ]

        response = HttpResponse(content='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'
        #work_book = xlwt.Workbook(encoding='utf-8')
        #work_sheet = work_book.add_sheet('Health Facilities')
        #row_num = 0
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([
                obj.facility_code, obj.name, obj.latitude, obj.longitude,
                obj.address, obj.settlement, obj.unit
            ])

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
