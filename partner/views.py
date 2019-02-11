# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Q
from wazimap.models import Geography
from . import models


# Create your views here.
def partner_profile(request, geo_name, org_slug):
    """
    Show the whole profile for an organisation
    """
    partner = models.Partner\
                   .objects\
                   .get(slug=org_slug)

    activities = models.Activity\
                 .objects\
                 .order_by('activity_number')\
                 .filter(Q(partner__slug=org_slug),
                         Q(province=geo_name)| Q(province="All provinces"))
    activity_numbers = []
    if not activities:
        location_activities = models.Location\
                     .objects\
                     .filter(location_name=geo_name, partner=partner)\
                     .values('activity_number')
        activity_numbers = [
            act_no['activity_number'] for act_no in location_activities
        ]
        activities = models.Activity\
                     .objects\
                     .order_by('activity_number')\
                     .filter(partner__slug=org_slug,
                             activity_number__in=activity_numbers)

    for activity in activities:
        activity_numbers.append(activity.activity_number)

    basic_ed = models.BasicEducationFacility.objects.filter(
        partner=partner, activity_number__in=activity_numbers)
    higher_ed = models.HigherEducationFacility.objects.filter(
        partner=partner, activity_number__in=activity_numbers)
    health = models.HealthFacility.objects.filter(
        partner=partner, activity_number__in=activity_numbers)

    return render(
        request, 'partner/partner_profile.html', {
            'geo': geo_name,
            'partner': partner,
            'activities': activities,
            'basic_ed': basic_ed,
            'higher_ed': higher_ed,
            'health': health
        })
