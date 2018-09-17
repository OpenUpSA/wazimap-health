from rest_framework import serializers

from wazimap_health.models import HealthFacilities


class HealthFacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = HealthFacilities
        exclude = ('service', 'id')
