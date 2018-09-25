from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wazimap_health.models import HealthFacilities, HigherEducation, BasicEducation

from . import serializers


class PointView(APIView):
    """
    Get all the points within a particular geography
    """
    model = None
    model_serializer = None

    def get(self, request):
        self.geo_code = request.query_params.get('geo_code', None)
        self.facility_code = request.query_params.get('facility_code', None)
        if self.geo_code:
            query = self.model\
                    .objects\
                    .filter(geo_levels__overlap=[self.geo_code])
            serialize = self.model_serializer(query, many=True)
            return Response({'data': serialize.data})
        elif self.facility_code:
            query = self.model.objects.get(facility_code=self.facility_code)
            serialize = self.model_serializer(query)
            return Response({'data': serialize.data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HealthView(PointView):
    model = HealthFacilities
    model_serializer = serializers.HealthFacilitySerializer


class HigherEducationView(PointView):
    model = HigherEducation
    model_serializer = serializers.HigherEducationSerializer


class BasicEducationView(PointView):
    model = BasicEducation
    model_serializer = serializers.BasicEducationSerializer


class FacilityView(APIView):
    """
    View details about a particular facility
    """

    def get(self, request):
        facility_code = request.query_params.get('code', None)
        dataset = request.query_params.get('dataset', None)
        if facility_code and dataset:
            if dataset == 'health':
                model = HealthFacilities
                model_serializer = serializers.HealthFacilitySerializer
            elif dataset == 'education':
                if facility_code.startswith('BEI'):
                    model = BasicEducation
                    model_serializer = serializers.BasicEducationSerializer
                else:
                    model = HigherEducation
                    model_serializer = serializers.HigherEducationSerializer
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            query = model.objects.get(facility_code=facility_code)
            serialize = model_serializer(query)
            return Response({'data': serialize.data})
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class HealthFacilityView(APIView):
#     """
#     Show all the health facilities within a district
#     """
#     def get(self, request):
#         geo_code = request.query_params.get('geo_code', None)
#         facility_code = request.query_params.get('facility_code', None)
#         if geo_code:
#             query = HealthFacilities\
#                     .objects\
#                     .filter(geo_levels__overlap=[geo_code])
#             serialize = serializers.HealthFacilitySerializer(query, many=True)
#             return Response(
#                 {
#                     'data': serialize.data
#                 }
#             )
#         elif facility_code:
#             query = HealthFacilities.objects.get(facility_code=facility_code)
#             serialize = serializers.HealthFacilitySerializer(query)
#             return Response(
#                 {
#                     'data': serialize.data
#                 }
#             )
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

# class HigherEducationView(APIView):
#     """
#     Show all the higher education institutions within a municipality
#     """
#     def get(self, request):
#         geo_code = request.query_params.get('geo_code', None)
#         if geo_code:
#             query = HigherEducation\
#                     .objects\
#                     .filter(geo_levels__overlap=[geo_code])
#             serialize = serializers.HigherEducationSerializer(query, many=True)
#             return Response({
#                 'data': serialize.data
#             })
#         return Response(status=status.HTTP_400_BAD_REQUEST)
