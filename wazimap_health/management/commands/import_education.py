import csv

from django.core.management.base import BaseCommand, CommandError
from wazimap_health import models


class Command(BaseCommand):
    help = "Load the various education facilities"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('--dataset', action='store', dest='dataset')

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
                    basic_education(reader)
                else:
                    raise CommandError('Unknown education dataset')

        except Exception:
            raise


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
                      'name': row.pop('Other Campuses'),
                      'classification': row.pop('Classification'),
                      'latitude': row.pop('Latitude'),
                      'longitude': row.pop('Longitude'),
                      'institution': row.pop('Institution'),
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


def basic_education(reader):
    """
    Import basic education records
    """
    code_prefix = 'BEI'
    code = 24798
    for row in reader:
        try:
            print('Working on {}'.format(row['Institution_Name']))
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
                        'latitude': row.pop('GIS_Latitude'),
                        'longitude': row.pop('GIS_Longitude'),
                        'address': row.pop('StreetAddress'),
                        'special_need': row.pop('SpecialNeed'),
                        'dataset': 'basic_education',
                        'facility_code': '{}{}'.format(code_prefix, code),
                        'service': dict(row)
                    },
                    facility_code='{}{}'.format(code_prefix,
                                                code),
                )
            print('Saved')
            code += 1
        except Exception:
            print("Bad xy coordinates or bad data")
            raise
    print("The last Value is {}".format(code))
