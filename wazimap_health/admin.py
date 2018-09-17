from django.contrib import admin
from django import forms
from django_admin_hstore_widget.forms import HStoreFormField

from . import models


class HealthFacilityAdminForm(forms.ModelForm):
    service = HStoreFormField()

    class Meta:
        model = models.HealthFacilities
        exclude = ()


@admin.register(models.HealthFacilities)
class HealthFacilityAdmin(admin.ModelAdmin):
    form = HealthFacilityAdminForm
