import requests

from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import PublicHealthFacilities, MarieStopes, PrivatePharmacies

MAPIT_URL = "http://10.186.210.96:8000/point/4326/"


class Command(BaseCommand):
    help = "Search and import a geo code for a facility"

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)

    def handle(self, *args, **options):
        """
        Get the district geo code from mapit based on the faclities lat/lon
        """
        if options['model'] is None:
            raise CommandError('No Model specified')
        try:
            model = eval(options['model'])
            for facility in model.objects.all():
                lat = facility.latitude
                lon = facility.longitude
                url = MAPIT_URL + '{},{}?type=DC'.format(lon, lat)
                req = requests.get(url)
                geo = req.json()
                if geo:
                    for _, value in geo.items():
                        facility.parent_geo_code = value['codes']['MDB']
                        facility.save(update_fields=['parent_geo_code'])
                        self.stdout.write(self.style.SUCCESS("Geo Inserted"))
                else:
                    self.stdout.write(self.style.SUCCESS("No District found for"))
        except Exception as error:
            raise CommandError(error)
