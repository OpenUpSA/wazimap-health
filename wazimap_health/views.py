from django.shortcuts import render
from django.db.models import Q

from .models import Organisation, Activity, AreaImplementation


def organisation_profile(request, geo_name, org_slug):
    """
    Show the whole profile for an organisation
    """
    organisation = Organisation\
                   .objects\
                   .get(slug=org_slug)
    activities = Activity\
                 .objects\
                 .filter(Q(organisation__slug=org_slug),
                         Q(province=geo_name)|Q(province="All provinces"))

    return render(request, 'organisation_profile.html', {
        'geo': geo_name,
        'organisation': organisation,
        'activities': activities
    })
