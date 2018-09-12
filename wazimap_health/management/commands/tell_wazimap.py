from django.core.management.base import BaseCommand, CommandError

from wazimap_health.models import PublicHealthFacilities, MarieStopes
from wazimap.models import Geography


class Command(BaseCommand):
    help = "Tell wazimap about the point data"

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)

    def handle(self, *args, **kwargs):
        if kwargs['model'] is None:
            raise CommandError('No Model specified')
        try:
            model = eval(kwargs['model'])
            for facility in model.objects.all():
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
                            'Point Data added for {}'.format(facility.name)
                        )
                    )
        except Exception as error:
                raise CommandError(error)
