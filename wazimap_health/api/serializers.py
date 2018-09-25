from rest_framework import serializers

from wazimap_health.models import HealthFacilities, HigherEducation, BasicEducation


class HealthFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthFacilities
        exclude = ('service', 'id')


class HigherEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HigherEducation
        exclude = ('service', 'id')


class BasicEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicEducation
        exclude = ('id', )
