from __future__ import unicode_literals
import csv

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import admin as useradmin
from django.contrib.auth import models as admin_models
from django import forms
from django_admin_hstore_widget.forms import HStoreFormField
from django.http import HttpResponse, JsonResponse
from django.conf.urls import url
from django.shortcuts import render
from .csv_import import ProcessImport

from wazimap.models import (Geography, SimpleTable, Dataset, Release,
                            FieldTable, DBTable, FieldTableRelease,
                            SimpleTableRelease)
from . import models


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class HealthImportForm(CsvImportForm):
    DATASET_CHOICE = (('public_health', 'Public Health Facilities'),
                      ('private_pharmacies', 'Private Pharamacies'),
                      ('marie_stopes', 'Marie Stopes'))
    dataset = forms.ChoiceField(choices=DATASET_CHOICE)


class BasicImportForm(CsvImportForm):
    DATASET_CHOICE = (('basic_education', 'Basic Education'), )
    dataset = forms.ChoiceField(choices=DATASET_CHOICE)


class HigherImportForm(CsvImportForm):
    DATASET_CHOICE = (('higher_education', 'Higher Education'), )
    dataset = forms.ChoiceField(choices=DATASET_CHOICE)


class ExportImportMixin:
    csv_form = None

    def _get_facility_fields(self, obj):
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
                service = self._flattern(obj[i], separator)
                for j in service.keys():
                    facility[j] = service[j]
            else:
                facility[i] = obj[i]
        return facility

    def import_csv(self, request, form):
        """
        Import a csv file from a user
        """
        if request.method == 'POST' and request.is_ajax():
            form = form(request.POST, request.FILES)
            if form.is_valid():
                try:
                    dataset = form.cleaned_data['dataset']
                    csv_file = request.FILES['csv_file']
                    reader = csv.DictReader(csv_file)
                    process = ProcessImport(dataset, reader)
                    process.import_csv()
                    return JsonResponse({'status': 'ok'})
                except Exception as error:
                    return JsonResponse({
                        'status': 'error',
                        'form': str(error)
                    })
            else:
                return JsonResponse({
                    'status': 'error',
                    'form': form.errors.as_json()
                })
        form = form()
        payload = {"form": form}
        return render(request, "admin/csv_form.djhtml", payload)

    def export_csv(self, request, queryset, export_fields):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=export.csv'

        facility = queryset.values(*export_fields)[0]
        writer = csv.DictWriter(
            response, fieldnames=self._get_facility_fields(facility))
        writer.writeheader()
        for obj in queryset.values(*export_fields):
            q = self._flattern(obj, '__')
            writer.writerow({
                k: v.encode('utf8') if isinstance(v, unicode) else v
                for k, v in q.items()
            })

        return response


class HealthFacilityAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.HealthFacilities
        exclude = ()


class HealthFacilityAdmin(admin.ModelAdmin, ExportImportMixin):
    list_display = ('name', 'settlement', 'unit', 'facility_code', 'dataset',
                    'latitude', 'longitude', 'geo_levels')
    list_filter = ('dataset', 'settlement', 'unit')
    form = HealthFacilityAdminForm
    actions = ['export_csv']
    change_list_template = 'admin/health_changelist.djhtml'
    search_fields = ('name', )

    def export_csv(self, request, queryset):
        export_fields = ('name', 'address', 'latitude', 'longitude',
                         'settlement', 'unit', 'service', 'facility_code')
        return super(HealthFacilityAdmin, self).export_csv(
            request, queryset, export_fields)

    def import_csv(self, request):
        csv_form = HealthImportForm
        return super(HealthFacilityAdmin, self).import_csv(request, csv_form)

    export_csv.short_description = 'Export Health Facilities'

    def get_urls(self):
        urls = super(HealthFacilityAdmin, self).get_urls()
        custom_urls = [
            url(r'^import-health-csv/$',
                self.admin_site.admin_view(self.import_csv),
                name='import_health_csv')
        ]
        return custom_urls + urls


class HigherEducationAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.HigherEducation
        exclude = ()


class HigherEducationAdmin(admin.ModelAdmin, ExportImportMixin):
    list_display = ('name', 'classification', 'facility_code', 'latitude',
                    'longitude', 'geo_levels')
    list_filter = ('classification', )
    form = HigherEducationAdminForm
    actions = ['export_csv']
    change_list_template = 'admin/higher_ed_changelist.djhtml'
    search_fields = ('name', )

    def export_csv(self, request, queryset):
        export_fields = ('name', 'institution', 'classification',
                         'facility_code', 'service', 'latitude', 'longitude',
                         'address')
        return super(HigherEducationAdmin, self).export_csv(
            request, queryset, export_fields)

    export_csv.short_description = 'Export higher education institutions'

    def get_urls(self):
        urls = super(HigherEducationAdmin, self).get_urls()
        custom_urls = [
            url(r'^import-higher-education-csv/$',
                self.admin_site.admin_view(self.import_csv),
                name='import_higher_csv')
        ]
        return custom_urls + urls

    def import_csv(self, request):
        form = HigherImportForm
        return super(HigherEducationAdmin, self).import_csv(request, form)


class BasicEducationAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.BasicEducation
        exclude = ()


class BasicEducationAdmin(admin.ModelAdmin, ExportImportMixin):
    list_display = ('name', 'sector', 'phase', 'facility_code', 'latitude',
                    'longitude', 'geo_levels')
    list_filter = ('phase', 'sector', 'special_need')
    form = BasicEducationAdminForm
    actions = ['export_csv']
    change_list_template = 'admin/basic_ed_changelist.djhtml'
    search_fields = ('name', )

    def export_csv(self, request, queryset):
        export_fields = ('name', 'sector', 'phase', 'facility_code',
                         'special_need', 'address', 'service', 'latitude',
                         'longitude')
        return super(BasicEducationAdmin, self).export_csv(
            request, queryset, export_fields)

    export_csv.short_description = 'Export basic education institutions'

    def get_urls(self):
        urls = super(BasicEducationAdmin, self).get_urls()
        custom_urls = [
            url(r'^import-basic-education-csv/$',
                self.admin_site.admin_view(self.import_csv),
                name='import_basic_csv')
        ]
        return custom_urls + urls

    def import_csv(self, request):
        form = BasicImportForm
        return super(BasicEducationAdmin, self).import_csv(request, form)


class HealthAdminSite(AdminSite):
    site_title = 'Clinton Health Access Initiative'
    site_header = 'CHAI Administration'
    index_title = 'CHAI Admin'


#admin_site = HealthAdminSite()
admin.site.register(models.HealthFacilities, HealthFacilityAdmin)
admin.site.register(models.HigherEducation, HigherEducationAdmin)
admin.site.register(models.BasicEducation, BasicEducationAdmin)
# admin.site.register(Geography)
# admin.site.register(SimpleTable)
# admin.site.register(Release)
# admin.site.register(Dataset)
# admin.site.register(FieldTable)
# admin.site.register(DBTable)
# admin.site.register(FieldTableRelease)
# admin.site.register(SimpleTableRelease)
