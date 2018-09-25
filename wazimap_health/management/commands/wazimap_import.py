import requests

from django.core.management.base import BaseCommand, CommandError
from wazimap_health.models import HealthFacilities, HigherEducation, BasicEducation
from wazimap.models import Geography

MAPIT_URL = "http://10.186.210.96:8000/point/4326/"


class Command(BaseCommand):
    help = "Tell wazimap about the point data, and which muncipality is belongs"

    def add_arguments(self, parser):
        parser.add_argument('--model', action='store', dest='model')

    def handle(self, *args, **options):
        try:
            model = eval(options.get('model'))
            for facility in model.objects.all():
                url = MAPIT_URL + '{},{}?type=MN'.format(
                    facility.longitude, facility.latitude)
                req = requests.get(url)
                geo = req.json()
                if geo:
                    for _, value in geo.items():
                        Geography.objects.update_or_create(
                            {
                                'geo_code': facility.facility_code,
                                'geo_level': 'point',
                                'parent_level': 'municipality',
                                'parent_code': value['codes']['MDB'],
                                'name': facility.name,
                                'version': '2011'
                            },
                            geo_code=facility.facility_code)
                self.stdout.write(self.style.SUCCESS('Point Data added for'))
        except Exception as error:
            raise CommandError(error)
