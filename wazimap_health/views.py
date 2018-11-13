from django.shortcuts import render
from django.db.models import Q

from .models import Organisation, Activity, PartnerBasicEducation, PartnerHealth, PartnerHigherEducation
from wazimap.models import Geography


def organisation_profile(request, geo_name, org_slug):
    """
    Show the whole profile for an organisation
    """
    organisation = Organisation\
                   .objects\
                   .get(slug=org_slug)
    province = Geography\
               .objects\
               .values('geo_code')\
               .get(name=geo_name, version='2011')
    activities = Activity\
                 .objects\
                 .filter(Q(organisation__slug=org_slug),
                         Q(province=geo_name)| Q(province="All provinces"))
    activity_numbers = []
    for activity in activities:
        activity_numbers.append(activity.activity_number)

    basic_ed = PartnerBasicEducation.objects.filter(
        organisation=organisation,
        activity_number__in=activity_numbers,
        province=province['geo_code'])
    higher_ed = PartnerHigherEducation.objects.filter(
        organisation=organisation,
        activity_number__in=activity_numbers,
        province=province['geo_code'])
    health = PartnerHealth.objects.filter(
        organisation=organisation,
        activity_number__in=activity_numbers,
        province=province['geo_code'])

    return render(
        request, 'organisation_profile.html', {
            'geo': geo_name,
            'organisation': organisation,
            'activities': activities,
            'basic_ed': basic_ed,
            'higher_ed': higher_ed,
            'health': health
        })
