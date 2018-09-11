from rest_framework import serializers

from wazimap_health.models import PublicHealthFacilities


class PublicHealthFacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PublicHealthFacilities
        fields = '__all__'
