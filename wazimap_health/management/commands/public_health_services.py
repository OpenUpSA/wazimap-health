from django.core.management.base import BaseCommand, CommandError

from wazimap_health.models import PublicHealthFacilities


class Command(BaseCommand):
    help = "Import the services that a public health facility provides"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):
        """
        Go through each facility
        """
        return
