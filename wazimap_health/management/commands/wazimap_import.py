from django.core.management.base import BaseCommand, CommandError

from wazimap_health.models import (HealthFacilities)
from wazimap.models import Geography


class Command(BaseCommand):
    help = "Tell wazimap about the point data"

    def handle(self, *args, **kwargs):
        try:
            for facility in HealthFacilities.objects.all():
                Geography.objects.update_or_create(
                    {
                        'geo_code': facility.facility_code,
                        'geo_level': 'point',
                        'parent_level': 'district',
                        'parent_code': facility.parent_geo_code,
                        'name': facility.name,
                        'version': '2011'
                    },
                    geo_code=facility.facility_code
                )
                self.stdout.write(
                        self.style.SUCCESS(
                            'Point Data added for'
                        )
                    )
        except Exception as error:
                raise CommandError(error)
