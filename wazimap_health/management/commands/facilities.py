import csv

from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import HealthFacilities


class Command(BaseCommand):
    help = "Import facilities from csv files"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        parser.add_argument('--dataset', type=str, dest='dataset')
        parser.add_argument('--group', type=str, dest='group')

    def handle(self, *args, **kwargs):
        if kwargs['file'] is None or kwargs['dataset'] is None:
            raise CommandError("Enter a csv file and a dataset type")
        if kwargs['dataset'] == 'health' and kwargs['group'] is None:
            raise CommandError("Please select the health dataset group")
        else:
            self.stdout.write(self.style.SUCCESS("Processing health csv file"))
            self._health(kwargs['file'], kwargs['group'])

    def _health(self, csv_file, group):
        code_prefix = 'HSF'
        self.stdout.write(
            self.style.SUCCESS("Feching latest health facility ID"))
        try:
            facility_code = HealthFacilities.objects.latest('id').facility_code
        except HealthFacilities.DoesNotExist:
            latest_code = 1
        else:
            latest_code = int(facility_code.split('HSF')[1])
        with open(csv_file, 'r') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                HealthFacilities\
                    .objects\
                    .update_or_create(
                        {
                            'name': row.pop('Facility Name'),
                            'settlement': row.pop('Organization Unit Rural_Urban_Semi'),
                            'unit': row.pop('Organization Unit Type'),
                            'latitude': row.pop('Latitude'),
                            'longitude': row.pop('Longitude'),
                            'address': row.pop('Physical Address'),
                            'facility_code': '{}{}'.format(code_prefix, latest_code),
                            'dataset': group,
                            'service': dict(row)
                        },
                        facility_code='{}{}'.format(code_prefix, latest_code)
                    )
                self.stdout.write(self.style.SUCCESS("Facility Entered"))
                latest_code += 1
