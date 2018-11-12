from __future__ import unicode_literals

from django.db.models import Q
from wazimap_health.models import Activity


def get_organization(geo):
    """
    Get the organisation working within the province.
    """
    orgs = Activity\
           .objects\
           .filter((Q(province=geo) | Q(province='All provinces')))\
           .only('organisation')\
           .distinct('organisation')\
           .values('organisation__name', 'organisation__slug')

    return {'organisations': list(orgs), 'organisation_geo': geo.name}
