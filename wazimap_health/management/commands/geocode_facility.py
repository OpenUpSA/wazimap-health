import requests

from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import HealthFacilities

MAPIT_URL = "http://10.186.210.96:8000/point/4326/"


class Command(BaseCommand):
    help = "Search and import a geo code for a facility"

    def handle(self, *args, **options):
        """
        Get the district geo code from mapit based on the faclities lat/lon
        """
        try:
            for facility in HealthFacilities.objects.all():
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
                    self.stdout.write(self.style.ERROR("No District found for"))
        except Exception as error:
            raise CommandError(error)
