import requests

from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import HealthFacilities, HigherEducation

MAPIT_URL = "http://10.186.210.96:8000/point/4326/"


class Command(BaseCommand):
    help = "Search and find in which geographies a point belongs to"

    def add_arguments(self, parser):
        parser.add_argument('--model', action='store', dest='model')

    def handle(self, *args, **options):
        """
        Get the district geo code from mapit based on the faclities lat/lon
        """
        try:
            model = eval(options.get('model'))
            for facility in model.objects.all():
                codes = []
                lat = facility.latitude
                lon = facility.longitude
                url = MAPIT_URL + '{},{}?type=PR,DC,MN'.format(lon, lat)
                req = requests.get(url)
                geo = req.json()
                if geo:
                    for _, value in geo.items():
                        codes.append(value['codes']['MDB'])
                    facility.geo_levels = codes
                    facility.save(update_fields=['geo_levels'])
                    self.stdout.write(self.style.SUCCESS("Geo Inserted"))
                else:
                    self.stdout.write(self.style.ERROR("No Parent Found"))
        except Exception as error:
            raise CommandError(error)
