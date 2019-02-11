from django.shortcuts import render
from django.db.models import Q
from .models import (HigherEducation, BasicEducation, HealthFacilities)
from wazimap.models import Geography
from django_tables2 import tables


class HigherTable(tables.Table):
    class Meta:
        model = HigherEducation
        exclude = ('service', 'id', 'geo_levels')


class BasicTable(tables.Table):
    class Meta:
        model = BasicEducation
        exclude = ('service', 'id', 'geo_levels')


class HealthTable(tables.Table):
    class Meta:
        model = HealthFacilities
        exclude = ('service', 'id', 'geo_levels')


def show_facilities(request, geo_code, dataset):
    """
    Show all the facilities at a particular geo_level
    """
    geo = Geography\
               .objects\
               .get(geo_code=geo_code, version='2011')
    groups = {
        'higher_education': {
            'model': HigherEducation,
            'table': HigherTable,
            'name': 'Higher Education Institutions'
        },
        'basic_education': {
            'model': BasicEducation,
            'table': BasicTable,
            'name': 'Basic Education Institutions'
        },
        'health': {
            'model': HealthFacilities,
            'table': HealthTable,
            'name': 'Health Facilities'
        }
    }
    query = groups[dataset]['model']\
                 .objects\
                 .filter(geo_levels__overlap=[geo_code])
    table = groups[dataset]['table'](query)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request, 'facilities.djhtml', {
        'facilities': table,
        'geo': geo,
        'name': groups[dataset]['name']
    })
