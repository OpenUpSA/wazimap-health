from django.db.models import Q
from .models import Location, Activity
from django.conf import settings


def get_partners(geo):
    """
    We need to check in which areasa are the partners working in.
    We first check for province, then we check the munis and district regions
    """
    if geo.geo_level == 'province':
        partners = Activity\
               .objects\
               .filter((Q(province=geo) | Q(province='All provinces')))\
               .only('partner')\
               .distinct('partner')\
               .values('partner__name', 'partner__slug', 'partner__logo')
    else:
        partners = Location\
               .objects\
               .filter(location_code=geo.geo_code)\
               .only('partner')\
               .distinct('partner')\
               .values('partner__name', 'partner__slug', 'partner__logo')

    return {
        'partners': list(partners),
        'partner_geo': geo.name,
        'image_path': settings.MEDIA_URL
    }
