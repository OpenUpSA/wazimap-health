from wazimap_health.models import Organisation, AreaImplementation


def get_organization(geo):
    """
    Get the organisation working within the province.
    """
    orgs = AreaImplementation\
           .objects\
           .filter(province=geo)\
           .select_related('Organisation')\
           .only('organisation')\
           .values('organisation__name')
    return {}

    return {'organisations': orgs}
