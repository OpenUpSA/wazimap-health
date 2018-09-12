import csv


from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import (MarieStopes,
                                   MarieStopesFacilities)


class Command(BaseCommand):
    help = "Load Marie Stopes facilities from a csv file,"

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
        code_prefix = 'MS'
        code = 1
        with open(options['file'], 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    phf, created = MarieStopes\
                                   .objects\
                                   .update_or_create(
                                       {
                                           'name': row['Facility'],
                                           'settlement': row['Org Unit Rural_Urban_Semi'],
                                           'latitude': row['Latitude'],
                                           'longitude': row['Longitude'],
                                           'address': row['Physical Address'],
                                           'facility_code': '{}{}'.format(code_prefix, code)
                                       },
                                       facility_code='{}{}'.format(code_prefix, code)
                                   )
                    obj, created = MarieStopesFacilities\
                                   .objects\
                                   .update_or_create({
                                       'facility': phf,
                                       'oral_pills': row['Oral Pills (contraception)'],
                                       'injectables': row['Injectables'],
                                       'iud': row['IUDs (contraception)'],
                                       'female_sterialization': row['Female Sterilization (contraception)'],
                                       'male_sterialization': row['Male Sterilization (contraception)'],
                                       'std': row['STI Screenings'],
                                       'hiv_testing': row['HIV Testing'],
                                       'hiv_treatment': row['HIV Treatment (ART)'],
                                       'oral_prep': row['Oral PrEP'],
                                       'first_trimester': row['Termination of Pregnancy - 1st Trimester'],
                                       'second_trimester': row['Termination of Pregnancy - 2nd Trimester'],
                                       'implants': row['Implants (contraception)']
                                   },
                                                     facility=phf)
                    code += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Entered {}'.format(row['Facility']))
                    )
                except Exception as error:
                    raise CommandError(error)
