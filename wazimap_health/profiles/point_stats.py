import json
from wazimap_health.models import PublicHealthFacilities, PublicHealthServices
from django.db.models import Count
from django.core import serializers

TOTAL = 0


def get_public_facility(geo_code):
    return {
        'public_health_facilities_total': total_facilities(geo_code),
        'public_health_facilities_settlements': settlement_count(geo_code),
        'public_health_facilities_unit': unit_count(geo_code)
    }


def total_facilities(geo_code):
    total = PublicHealthFacilities\
                       .objects\
                       .filter(parent_geo_code=geo_code)\
                       .count()
    global TOTAL
    TOTAL = float(total)
    return {'values': {'this': total}, 'name': 'Total Facilities'}


def settlement_count(geo_code):
    count = PublicHealthFacilities\
                      .objects.values('settlement')\
                      .filter(parent_geo_code=geo_code)\
                      .annotate(total=Count('name'))\
                      .order_by('-total')
    stats = {}
    for totals in count:
        percent = (totals.values()[0] / TOTAL) * 100
        stats.update({
            totals.values()[1]: {'name': totals.values()[1],
                                 'numerators': {'this': totals.values()[0]},
                                 'values': {'this': percent}},
            'metadata': {'citation': '',
                         'release': '',
                         'table_id': '',
                         'universe': '',
                         'year': '2018'}
        })

    return stats


def unit_count(geo_code):
    count = PublicHealthFacilities\
                 .objects.values('unit')\
                 .filter(parent_geo_code=geo_code)\
                 .annotate(total=Count('name'))\
                 .order_by('-total')
    stats = {}
    for totals in count:
        percent = (totals.values()[0] / TOTAL) * 100
        stats.update({
            totals.values()[1]: {'name': totals.values()[1],
                                 'numerators': {'this': totals.values()[0]},
                                 'values': {'this': percent}},
            'metadata': {'citation': '',
                         'release': '',
                         'table_id': '',
                         'universe': '',
                         'year': '2018'}
        })
    return stats



def get_facility_services(geo_code):
    query = PublicHealthServices\
            .objects\
            .filter(facility__facility_code=geo_code)
    data = serializers.serialize('json', query)
    model_data = json.loads(data)
    return {'services': model_data[0]['fields']}
