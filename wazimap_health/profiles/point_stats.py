import json
from django.db.models import Count
from django.core import serializers

from wazimap_health.models import HealthFacilities

TOTAL = 0


def get_heath_details(geo_code):
    return {
        'public_health_total': facility_total(geo_code, 'public_facilities'),
        'public_health_settlement': facility_settlement(geo_code,
                                                        'public_facilities'),
        'public_health_unit': facility_unit(geo_code, 'public_facilities'),
        'pharmacy_total': facility_total(geo_code, 'private_pharmacies'),
        'pharmacy_settlement': facility_settlement(geo_code,
                                                   'private_pharmacies'),
        'pharmacy_unit': facility_unit(geo_code, 'private_pharmacies'),
        'marie_stopes_total': facility_total(geo_code, 'marie_stopes'),
        'marie_stopes_settlement': facility_settlement(geo_code, 'marie_stopes')
    }


def facility_total(geo_code, dataset):
    name = {
        'public_facilities': 'Total Public Health Facilities',
        'private_pharmacies': 'Total Private Pharmacies',
        'marie_stopes': 'Total Marie Stopes Facilities'
    }
    total = HealthFacilities\
                       .objects\
                       .filter(geo_levels__overlap=[geo_code],
                               dataset=dataset)\
                       .count()
    global TOTAL
    TOTAL = 0
    TOTAL = float(total)
    return {'values': {'this': total},
            'name': name[dataset]}

def facility_settlement(geo_code, dataset):
    """
    Return totals about the type of settlements
    """
    count = HealthFacilities\
                      .objects.values('settlement')\
                      .filter(geo_levels__overlap=[geo_code],
                              dataset=dataset)\
                      .annotate(total=Count('name'))\
                      .order_by('-total')
    stats = {}
    for result in count:
        percent = (result['total'] / TOTAL) * 100
        stats.update({
            result['settlement'] or 'Unclassified': {'name': result['settlement'] or 'Unclassified',
                                                   'numerators': {'this': result['total']},
                                                   'values': {'this': percent}},
            'metadata': {'citation': '',
                         'release': '',
                         'table_id': '',
                         'universe': '',
                         'year': '2018'}
        })

    return stats


def facility_unit(geo_code, dataset):
    """
    Return totals for the unit types
    """
    count = HealthFacilities\
                 .objects.values('unit')\
                 .filter(geo_levels__overlap=[geo_code],
                         dataset=dataset)\
                 .annotate(total=Count('name'))\
                 .order_by('-total')
    stats = {}
    for result in count:
        percent = (result['total']/ TOTAL) * 100
        stats.update({
            result['unit'] or 'Unclassified': {'name': result['unit'] or 'Unclassified',
                                 'numerators': {'this': result['total']},
                                 'values': {'this': percent}},
            'metadata': {'citation': '',
                         'release': '',
                         'table_id': '',
                         'universe': '',
                         'year': '2018'}
        })
    return stats



def get_facility_services(geo_code):
    """
    Choose the models created by the code
    PPF = Private Pharmacies
    PHF = Public Health Facilities
    MSS = Marie Stopes
    """
    query = HealthFacilities\
            .objects\
            .filter(facility_code=geo_code)
    data = serializers.serialize('json', query)
    model_data = json.loads(data)
    service = model_data[0]['fields']
    return {'services': json.loads(service['service'])}
