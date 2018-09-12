import csv


from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import (PublicHealthFacilities,
                                   PublicHealthServices)


class Command(BaseCommand):
    help = "Load public health facilities from a csv file,"

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
                    phf, created = PublicHealthFacilities\
                                   .objects\
                                   .update_or_create(
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
                    obj, created = PublicHealthServices\
                                   .objects\
                                   .update_or_create({
                                       'facility': phf,
                                       'oral_pills': row['Oral Pills (contraception)'],
                                       'injectables': row['Injectables'],
                                       'iud': row['IUDs (contraception)'],
                                       'female_sterialization': row['Female Sterilization (contraception)'],
                                       'male_sterialization': row['Male Sterilization (contraception)'],
                                       'male_circumcision': row['Male Medical Circumcision (MMC)'],
                                       'tb': row['TB'],
                                       'maternal_health': row['Maternal Health'],
                                       'mental_health': row['Mental Health'],
                                       'child_health': row['Child Health'],
                                       'oral_health': row['Oral health services'],
                                       'rehabilitation': row['Rehabilitation Services'],
                                       'minor_ailments': row['Minor Ailments'],
                                       'std': row['Sexually Transmitted Infections Screenings'],
                                       'hiv_testing': row['HIV Testing'],
                                       'hiv_treatment': row['HIV Treatment (ART)'],
                                       'oral_prep': row['Oral PrEP'],
                                       'first_trimester': row['Termination of Pregnancy - 1st Trimester'],
                                       'second_trimester': row['Termination of Pregnancy - 2nd Trimester'],
                                       'ayfs': row['AYFS Accredited'],
                                       'ccmdd_pick': row['CCMDD Pick Up Point'],
                                       'status': row['Status'],
                                       'implants': row['Implants (contraception)']
                                   },
                                                     facility=phf)
                    code += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Entered {}'.format(row['Facility Name_2']))
                    )
                except Exception as error:
                    raise CommandError(error)
