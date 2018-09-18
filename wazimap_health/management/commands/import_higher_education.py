import csv


from django.core.management.base import BaseCommand, CommandError
from wazimap_health import health_facilities, models


class Command(BaseCommand):
    help = "Load the various health facilities"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):

        if kwargs['file'] is None:
            raise CommandError("No Higher education file selected")
        try:
            code_prefix = 'HEI'
            with open(kwargs['file'], 'r') as data_file:
                reader = csv.DictReader(data_file)
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
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Institution Addded'
                        )
                    )
                    code += 1
        except Exception as error:
            raise CommandError(error)
