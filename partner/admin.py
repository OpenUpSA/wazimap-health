# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from wazimap_health.admin import HealthAdminSite
from partner.process import process_excelsheet
from partner.forms import PartnerForm
from partner import models
from django.http import JsonResponse
from django.shortcuts import render
from django.conf.urls import url


class PartnerAdmin(admin.ModelAdmin):
    change_list_template = 'partner/partner_changelist.djhtml'

    def import_partner_sheet(self, request):
        if request.method == 'POST' and request.is_ajax():
            form = PartnerForm(request.POST, request.FILES)
            if form.is_valid():
                logo = request.FILES['logo']
                excel_sheet = request.FILES['excel_sheet']
                try:
                    process_excelsheet(logo, excel_sheet)
                    return JsonResponse({
                        'status': 'ok',
                    })
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

        form = PartnerForm()
        return render(request, 'partner/upload_partner_sheet.djhtml',
                      {'form': form})

    def get_urls(self):
        urls = super(PartnerAdmin, self).get_urls()
        custom_urls = [
            url(r'^upload-partner-template$',
                self.admin_site.admin_view(self.import_partner_sheet),
                name='import_partner_sheet')
        ]
        return custom_urls + urls


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('partner', 'activity', 'activity_number')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('partner', 'name')


class BasicEducationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'school', 'activity_number', 'province')


class HealthAdmin(admin.ModelAdmin):
    list_display = ('partner', 'facility', 'activity_number', 'province')


class HigherEducationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'campus', 'activity_number', 'province')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'location_code', 'location_name',
                    'activity_number')


admin_site = HealthAdminSite()
admin.site.register(models.Partner, PartnerAdmin)
admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.BasicEducationFacility, BasicEducationAdmin)
admin.site.register(models.HigherEducationFacility, HigherEducationAdmin)
admin.site.register(models.HealthFacility, HealthAdmin)
admin.site.register(models.Location, LocationAdmin)
