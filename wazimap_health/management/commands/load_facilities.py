import csv


from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import PublicHealthFacilities


class Command(BaseCommand):
    help = "Load the facilities from a csv file,"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)
        
    def handle(self, *args, **options):
        """
        * Add facilities
        * Generate a random unique code for a facility.
        * This unique code is only for wazimap, the codes have no meaning
        outside of wazimap
        """
        if options['file'] is None:
            raise CommandError('No facility file specified')
        print(options['file'])
        code_prefix = 'PHF'
        code = 1
        with open(options['file'], 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    PublicHealthFacilities.objects.update_or_create(
                        {
                            'name': row['Facility Name_2'],
                            'settlement': row['Organization Unit Rural_Urban_Semi'],
                            'unit': row['Organization Unit Type'],
                            'latitude': row['Latitude'],
                            'longitude': row['Longitude'],
                            'facility_code': '{}{}'.format(code_prefix, code)
                        },
                        facility_code='{}{}'.format(code_prefix, code)
                                                                    
                    )
                    code += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Entered {}'.format(row['Facility Name_2']))
                    )
                except Exception as error:
                    raise CommandError(error)
