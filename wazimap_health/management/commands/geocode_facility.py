import requests

from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import PublicHealthFacilities

MAPIT_URL = "http://10.186.210.96:8000/point/4326/"


class Command(BaseCommand):
    help = "Search and import a geo code for a facility"

    def handle(self, *args, **options):
        """
        Get the district geo code from mapit based on the faclities lat/lon
        """
        for facility in PublicHealthFacilities.objects.all():
            lat = facility.latitude
            lon = facility.longitude
            url = MAPIT_URL + '{},{}?type=DC'.format(lon, lat)
            print(url)
            try:
                req = requests.get(url)
            except Exception as error:
                print(error)
                exit()
            else:
                geo = req.json()
                if geo:
                    for _, value in geo.items():
                        print(value['codes']['MDB'])
                        facility.parent_geo_code = value['codes']['MDB']
                        facility.save(update_fields=['parent_geo_code'])
                        self.stdout.write(self.style.SUCCESS("Geo Inserted"))
                else:
                    self.stdout.write(self.style.SUCCESS("No District found for  {}".format(facility.name)))
