from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wazimap_health.models import HealthFacilities

from . import serializers


class HealthFacilityView(APIView):
    """
    Show all the health facilities within a district
    """
    def get(self, request):
        geo_code = request.query_params.get('geo_code', None)
        facility_code = request.query_params.get('facility_code', None)
        if geo_code:
            query = HealthFacilities.objects.filter(parent_geo_code=geo_code)
            serialize = serializers.HealthFacilitySerializer(query, many=True)
            return Response(
                {
                    'data': serialize.data
                }
            )
        elif facility_code:
            query = HealthFacilities.objects.get(facility_code=facility_code)
            serialize = serializers.HealthFacilitySerializer(query)
            return Response(
                {
                    'data': serialize.data
                }
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
