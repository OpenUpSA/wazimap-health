import json
from django.db.models import Count
from django.core import serializers

from wazimap_health.models import HealthFacilities, HigherEducation, BasicEducation

TOTAL = 0

CITATIONS = {
    'private_pharmacies': 'Independent Community Pharmacy Association',
    'public_health':
    'DHIS-The District Health Information System ( 2017-2018)',
    'marie_stopes': 'DHIS-The District Health Information System ( 2017-2018)',
}


def get_heath_details(geo_code):
    return {
        'public_health_total':
        facility_total(geo_code, 'public_health'),
        'public_health_settlement':
        facility_settlement(geo_code, 'public_health'),
        'public_health_unit':
        facility_unit(geo_code, 'public_health'),
        'pharmacy_total':
        facility_total(geo_code, 'private_pharmacies'),
        'pharmacy_settlement':
        facility_settlement(geo_code, 'private_pharmacies'),
        'pharmacy_unit':
        facility_unit(geo_code, 'private_pharmacies'),
        'marie_stopes_total':
        facility_total(geo_code, 'marie_stopes'),
        'marie_stopes_settlement':
        facility_settlement(geo_code, 'marie_stopes')
    }


def get_higher_ed_details(geo_code):
    return {
        'higher_education_total': higher_ed_total(geo_code),
        'higher_education_classification': higher_ed_classification(geo_code),
        'higher_education_campus': get_institution_campuses(geo_code)
    }


def get_basic_education_details(geo_code):
    """
    Get information related to basic education
    """
    return {
        'basic_education_total': basic_education_total(geo_code),
        'basic_education_phase': basic_education_phase(geo_code),
        'basic_education_sector': basic_education_sector(geo_code)
    }


def facility_total(geo_code, dataset):
    name = {
        'public_health': 'Total Public Health Facilities',
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
    return {'values': {'this': total}, 'name': name[dataset]}


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
            result['settlement'] or 'Unclassified': {
                'name': result['settlement'] or 'Unclassified',
                'numerators': {
                    'this': result['total']
                },
                'values': {
                    'this': percent
                }
            },
            'metadata': {
                'citation': CITATIONS[dataset],
                'release': CITATIONS[dataset],
                'table_id': '',
                'universe': '',
                'year': '2018'
            }
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
        percent = (result['total'] / TOTAL) * 100
        stats.update({
            result['unit'] or 'Unclassified': {
                'name': result['unit'] or 'Unclassified',
                'numerators': {
                    'this': result['total']
                },
                'values': {
                    'this': percent
                }
            },
            'metadata': {
                'citation': CITATIONS[dataset],
                'release': CITATIONS[dataset],
                'table_id': '',
                'universe': '',
                'year': '2018'
            }
        })
    return stats


def get_facility_services(geo_code):
    """
    Choose the models created by the code
    PPF = Private Pharmacies Facilities
    PHF = Public Health Facilities
    MSS = Marie Stopes
    HEI = Higher Education Institutions
    """
    if geo_code.startswith('HEI'):
        model = HigherEducation
    elif geo_code.startswith('BEI'):
        model = BasicEducation
    else:
        model = HealthFacilities

    query = model\
            .objects\
            .filter(facility_code=geo_code)
    data = serializers.serialize('json', query)
    model_data = json.loads(data)
    detail = model_data[0]['fields']
    if geo_code.startswith('HSF'):
        info = {
            'settlement': detail['settlement'],
            'unit': detail['unit'],
            'address': detail['address'],
            'service': json.loads(detail['service'])
        }
    elif geo_code.startswith('BEI'):
        info = {
            'sector': detail['sector'],
            'phase': detail['phase'],
            'address': detail['address'],
            'special_need': detail['special_need']
        }
    elif geo_code.startswith('HEI'):
        info = {
            'institution': detail['institution'],
            'classification': detail['classification'],
            'address': detail['address']
        }

    return info


def get_institution_campuses(geo_code):
    if geo_code.startswith('HEI'):
        place = HigherEducation.objects.get(facility_code=geo_code)
        campuses = HigherEducation\
                   .objects\
                   .only('name')\
                   .filter(institution=place.institution)\
                   .exclude(facility_code=place.facility_code)
        data = serializers.serialize('json', campuses)
        model_data = json.loads(data)
        institution = {}
        detail = []
        for campus in model_data:
            detail.append({'name': campus['fields']['name']})
        institution['campus'] = detail
        institution['info'] = {
            'institution': place.institution,
            'classification': place.classification,
            'address': place.address
        }
        return institution


def higher_ed_total(geo_code):
    """
    Get the total number of insitutions within a geo area
    """
    total = HigherEducation\
            .objects\
            .filter(geo_levels__overlap=[geo_code])\
            .count()
    global HIGHER_TOTAL
    HIGHER_TOTAL = 0
    HIGHER_TOTAL = float(total)
    return {
        'values': {
            'this': total
        },
        'name': 'Total Higher Education Institutions'
    }


def higher_ed_classification(geo_code):
    """
    Return the totals for the various classifications within insitutions
    """
    count = HigherEducation\
                 .objects.values('classification')\
                 .filter(geo_levels__overlap=[geo_code])\
                 .annotate(total=Count('name'))\
                 .order_by('-total')
    stats = {}
    for result in count:
        percent = (result['total'] / HIGHER_TOTAL) * 100
        stats.update({
            result['classification'] or 'Unclassified': {
                'name': result['classification'] or 'Unclassified',
                'numerators': {
                    'this': result['total']
                },
                'values': {
                    'this': percent
                }
            },
            'metadata': {
                'citation': 'DHET',
                'release': 'Department of Higher Education and Training',
                'table_id': '',
                'universe': '',
                'year': '2018'
            }
        })
    if stats:
        return stats
    else:
        stats.update({
            'metadata': {
                'citation': 'DHET',
                'release': 'Department of Higher Education and Training',
                'table_id': '',
                'universe': '',
                'year': '2018'
            }
        })
        return stats


def basic_education_total(geo_code):
    """
    Return the total of basic education institutions
    """
    total = BasicEducation\
            .objects\
            .filter(geo_levels__overlap=[geo_code])\
            .count()
    global BASIC_TOTAL
    BASIC_TOTAL = 0
    BASIC_TOTAL = float(total)
    return {
        'values': {
            'this': total
        },
        'name': 'Total Basic Education Institutions'
    }


def basic_education_phase(geo_code):
    """
    Collect the various type of basic education phases
    """
    count = BasicEducation\
            .objects\
            .values('phase')\
            .filter(geo_levels__overlap=[geo_code])\
            .annotate(total=Count('name'))\
            .order_by('-total')
    stats = {}
    for result in count:
        percent = (result['total'] / BASIC_TOTAL) * 100
        stats.update({
            result['phase'] or 'Unclassified': {
                'name': result['phase'] or 'Unclassified',
                'numerators': {
                    'this': result['total']
                },
                'values': {
                    'this': percent
                }
            },
            'metadata': {
                'citation': 'DBE (2017)',
                'release': 'National Department of Basic Education',
                'table_id': '',
                'universe': '',
                'year': '2018'
            }
        })
    return stats


def basic_education_sector(geo_code):
    """
    Count the various basic education sectors
    """
    count = BasicEducation\
            .objects\
            .values('sector')\
            .filter(geo_levels__overlap=[geo_code])\
            .annotate(total=Count('name'))\
            .order_by('-total')
    stats = {}
    for result in count:
        percent = (result['total'] / BASIC_TOTAL) * 100
        stats.update({
            result['sector'] or 'Unclassified': {
                'name': result['sector'] or 'Unclassified',
                'numerators': {
                    'this': result['total']
                },
                'values': {
                    'this': percent
                }
            },
            'metadata': {
                'citation': 'DBE (2017)',
                'release': 'National Department of Basic Education',
                'table_id': '',
                'universe': '',
                'year': '2018'
            }
        })
    return stats
