import csv


from django.core.management.base import BaseCommand, CommandError
from wazimap_health import health_facilities


class Command(BaseCommand):
    help = "Load the various health facilities"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('dataset', type=str)

    def handle(self, *args, **kwargs):

        if kwargs['file'] is None or kwargs['dataset'] is None:
            raise CommandError("File and Dataset needed")
        if kwargs['dataset'] == 'pharmacies':
            code_prefix = 'PPF'
        elif kwargs['dataset'] == 'public_facilities':
            code_prefix = 'PHF'
        elif kwargs['dataset'] == 'marie_stopes':
            code_prefix = 'MSS'
        else:
            raise CommandError('Uknown dataset')

        try:
            with open(kwargs['file'], 'r') as data_file:
                reader = csv.DictReader(data_file)
                if kwargs['dataset'] == 'pharmacies':
                    health_facilities.pharmacies(reader, code_prefix)
                elif kwargs['dataset'] == 'public_facilities':
                    health_facilities.public_facilities(reader, code_prefix)
                elif kwargs['dataset'] == 'marie_stopes':
                    health_facilities.marie_stopes(reader, code_prefix)
                else:
                    raise CommandError("Unknown Dataset")
        except Exception as error:
            raise CommandError(error)
