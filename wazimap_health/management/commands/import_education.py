import csv

from django.core.management.base import BaseCommand, CommandError
from wazimap_health import models


class Command(BaseCommand):
    help = "Load the various education facilities"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('--dataset', action='store', dest='dataset')
        parser.add_argument('--type', action='store', dest='type')

    def handle(self, *args, **kwargs):

        if kwargs['file'] is None or kwargs['dataset'] is None:
            raise CommandError(
                "No Higher education file selected or Dataset selected")
        try:
            with open(kwargs['file'], 'r') as data_file:
                reader = csv.DictReader(data_file)
                if kwargs['dataset'] == 'higher_education':
                    higher_education(reader)
                elif kwargs['dataset'] == 'basic_education':
                    basic_education(reader, kwargs['type'])
                else:
                    raise CommandError('Unknown education dataset')

        except Exception as error:
            raise CommandError(error)


def higher_education(reader):
    """
    Import higher education records
    """
    code_prefix = 'HEI'
    code = 1
    for row in reader:
        row.pop('Province')
        models.HigherEducation\
              .objects\
              .update_or_create(
                  {
                      'name': row.pop('School Name'),
                      'classification': row.pop('Classification'),
                      'latitude': row.pop('Latitude'),
                      'longitude': row.pop('Longitude'),
                      'institution': row.pop('District'),
                      'address': row.pop('Physical Address'),
                      'dataset': 'higher_education',
                      'facility_code': '{}{}'.format(code_prefix, code),
                      'service': dict(row)
                  },
                  facility_code='{}{}'.format(code_prefix, code)
              )
        print("Saved")
        code += 1
    return


def basic_education(reader, education_type):
    """
    Import basic education records
    """
    education_code = {'special': 'SBEI', 'ordinary': 'BEI'}
    dataset = {
        'special': 'special_needs_education',
        'ordinary': 'basic_education'
    }
    code = 1
    for row in reader:
        row.pop('Province')
        row.pop('LMunName')
        row.pop('DMunName')
        models.BasicEducation\
            .objects\
            .update_or_create(
                {
                    'name': row.pop('Institution_Name'),
                    'sector': row.pop('Sector'),
                    'phase': row.pop('Phase') or '',
                    'latitude': row.pop('GIS_Lat'),
                    'longitude': row.pop('GIS_Long'),
                    'address': row.pop('StreetAddress'),
                    'dataset': dataset[education_type],
                    'facility_code': '{}{}'.format(
                        education_code[education_type],
                        code),
                    'service': dict(row)
                },
                facility_code='{}{}'.format(education_code[education_type],
                                            code)
            )
        print('Saved')
        code += 1
    return
