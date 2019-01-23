from __future__ import unicode_literals

from django.db.models import Q
from wazimap_health.models import Activity, PartnerLocation


def get_organization(geo):
    """
    We need to check in which areasa are the organisations working in.
    We first check for province, then we check the munis and district regions
    """
    if geo.geo_level == 'province':
        orgs = Activity\
               .objects\
               .filter((Q(province=geo) | Q(province='All provinces')))\
               .only('organisation')\
               .distinct('organisation')\
               .values('organisation__name', 'organisation__slug')
    else:
        orgs = PartnerLocation\
               .objects\
               .filter(location_code=geo.geo_code)\
               .only('organisation')\
               .distinct('organisation')\
               .values('organisation__name', 'organisation__slug')

    return {'organisations': list(orgs), 'organisation_geo': geo.name}
