from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wazimap_health.models import (PublicHealthFacilities,
                                   PublicHealthServices)

from . import serializers


class PublicFacilityView(APIView):
    """
    Show all the Public health Facilities within a Geography
    """
    def get(self, request):
        parent_geo_code = request.query_params.get('parent_geo_code', None)
        facility = request.query_params.get('facility', None)
        if parent_geo_code is None and facility is None:
            return Response(status.HTTP_400_BAD_REQUEST)
        if parent_geo_code:
            query = PublicHealthFacilities\
                    .objects\
                    .filter(parent_geo_code=parent_geo_code)
            serialize = serializers.PublicHealthFacilitySerializer(query,
                                                               many=True)
            return Response(
                {'data': serialize.data}
            )
        if (facility):
            query = PublicHealthFacilities\
                    .objects\
                    .get(facility_code=facility)
            serialize = serializers.PublicHealthFacilitySerializer(query)
            return Response({
                'data': serialize.data
            })


class PublicServicesView(APIView):
    """
    Show all the services a particular health service has
    """
    def get(self, request, code):
        query = PublicHealthServices\
                .objects\
                .get(facility__facility_code=code)
        serialize = serializers.PublicServicesSerializer(query)
        return Response(serialize.data)
