from django.shortcuts import render
from django.db.models import Q
from .models import (Organisation, Activity, PartnerBasicEducation,
                     PartnerHealth, PartnerHigherEducation, PartnerLocation,
                     HigherEducation, BasicEducation, HealthFacilities)
from wazimap.models import Geography
from django_tables2 import tables


class HigherTable(tables.Table):
    class Meta:
        model = HigherEducation
        exclude = ('service', 'id', 'geo_levels')


class BasicTable(tables.Table):
    class Meta:
        model = BasicEducation
        exclude = ('service', 'id', 'geo_levels')


class HealthTable(tables.Table):
    class Meta:
        model = HealthFacilities
        exclude = ('service', 'id', 'geo_levels')


def organisation_profile(request, geo_name, org_slug):
    """
    Show the whole profile for an organisation
    """
    organisation = Organisation\
                   .objects\
                   .get(slug=org_slug)
    geo_area = Geography\
               .objects\
               .values('geo_code')\
               .get(name=geo_name, version='2011')
    activities = Activity\
                 .objects\
                 .order_by('activity_number')\
                 .filter(Q(organisation__slug=org_slug),
                         Q(province=geo_name)| Q(province="All provinces"))
    activity_numbers = []
    if not activities:
        location_activities = PartnerLocation\
                     .objects\
                     .filter(location_name=geo_name, organisation=organisation)\
                     .values('activity_number')
        activity_numbers = [
            act_no['activity_number'] for act_no in location_activities
        ]
        activities = Activity\
                     .objects\
                     .order_by('activity_number')\
                     .filter(organisation__slug=org_slug,
                             activity_number__in=activity_numbers)

    for activity in activities:
        activity_numbers.append(activity.activity_number)

    basic_ed = PartnerBasicEducation.objects.filter(
        organisation=organisation, activity_number__in=activity_numbers)
    higher_ed = PartnerHigherEducation.objects.filter(
        organisation=organisation, activity_number__in=activity_numbers)
    health = PartnerHealth.objects.filter(
        organisation=organisation, activity_number__in=activity_numbers)

    return render(
        request, 'organisation_profile.html', {
            'geo': geo_name,
            'organisation': organisation,
            'activities': activities,
            'basic_ed': basic_ed,
            'higher_ed': higher_ed,
            'health': health
        })


def show_facilities(request, geo_code, dataset):
    """
    Show all the facilities at a particular geo_level
    """
    geo = Geography\
               .objects\
               .get(geo_code=geo_code, version='2011')
    groups = {
        'higher_education': {
            'model': HigherEducation,
            'table': HigherTable,
            'name': 'Higher Education Institutions'
        },
        'basic_education': {
            'model': BasicEducation,
            'table': BasicTable,
            'name': 'Basic Education Institutions'
        },
        'health': {
            'model': HealthFacilities,
            'table': HealthTable,
            'name': 'Health Facilities'
        }
    }
    query = groups[dataset]['model']\
                 .objects\
                 .filter(geo_levels__overlap=[geo_code])
    table = groups[dataset]['table'](query)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'facilities.djhtml', {
        'facilities': table,
        'geo': geo,
        'name': groups[dataset]['name']
    })
