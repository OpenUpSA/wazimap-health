import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wazimap.models import Geography
from wazimap_health.models import HealthFacilities, HigherEducation, BasicEducation
from django.conf import settings
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


class HealthServiceView(APIView):
    """
    List all the possible Health Services
    """

    def get(self, request):
        return Response({
            'services': [{
                'id': '001',
                'name': 'Oral Pills (contraception)'
            }, {
                'id': '002',
                'name': 'Injectables'
            }, {
                'id': '003',
                'name': 'IUDs  (contraception)'
            }, {
                'id': '004',
                'name': 'Implants (contraception)'
            }, {
                'id': '005',
                'name': 'Female Sterilization (contraception)'
            }, {
                'id': '006',
                'name': 'Male Sterilization (contraception)'
            }, {
                'id': '007',
                'name': 'Male Medical Circumcision (MMC)'
            }, {
                'id': '008',
                'name': 'TB'
            }, {
                'id': '009',
                'name': 'Maternal Health'
            }, {
                'id': '010',
                'name': 'Mental Health'
            }, {
                'id': '011',
                'name': 'Child Health'
            }, {
                'id': '012',
                'name': 'Oral health services'
            }, {
                'id': '013',
                'name': 'Rehabilitation Services'
            }, {
                'id': '014',
                'name': 'Minor Ailments'
            }, {
                'id': '015',
                'name': 'Sexually Transmitted Infections Screenings'
            }, {
                'id': '016',
                'name': 'HIV Testing'
            }, {
                'id': '017',
                'name': 'HIV Treatment (ART)'
            }, {
                'id': '018',
                'name': 'Oral PrEP'
            }, {
                'id': '019',
                'name': 'Termination of Pregnancy - 1st Trimester'
            }, {
                'id': '020',
                'name': 'Termination of Pregnancy - 2nd Trimester'
            }, {
                'id': '021',
                'name': 'AYFS Accredited'
            }, {
                'id': '022',
                'name': 'CCMDD Pick Up Point'
            }]
        })
        return Response({
            'services': {
                '001': 'Oral Pills (contraception)',
                '002': 'Injectables',
                '003': 'IUDs  (contraception)',
                '004': 'Implants (contraception)',
                '005': 'Female Sterilization (contraception)',
                '006': 'Male Sterilization (contraception)',
                '007': 'Male Medical Circumcision (MMC)',
                '008': 'TB',
                '009': 'Maternal Health',
                '010': 'Mental Health',
                '011': 'Child Health',
                '012': 'Oral health services',
                '013': 'Rehabilitation Services',
                '014': 'Minor Ailments',
                '015': 'Sexually Transmitted Infections Screenings',
                '016': 'HIV Testing',
                '017': 'HIV Treatment (ART)',
                '018': 'Oral PrEP',
                '019': 'Termination of Pregnancy - 1st Trimester',
                '020': 'Termination of Pregnancy - 2nd Trimester',
                '021': 'AYFS Accredited',
                '022': 'CCMDD Pick Up Point',
            },
        })


class ServiceView(APIView):
    """
    Find all the facilities that have a particular service.

    This will also depend on the users location
    
    ***The users location should be provided as a query paramater with latitude longitude***
    
    ```
    ?location=lat,lon
    ```
    

    """

    services = {
        '001': 'Oral Pills (contraception)',
        '002': 'Injectables',
        '003': 'IUDs  (contraception)',
        '004': 'Implants (contraception)',
        '005': 'Female Sterilization (contraception)',
        '006': 'Male Sterilization (contraception)',
        '007': 'Male Medical Circumcision (MMC)',
        '008': 'TB',
        '009': 'Maternal Health',
        '010': 'Mental Health',
        '011': 'Child Health',
        '012': 'Oral health services',
        '013': 'Rehabilitation Services',
        '014': 'Minor Ailments',
        '015': 'Sexually Transmitted Infections Screenings',
        '016': 'HIV Testing',
        '017': 'HIV Treatment (ART)',
        '018': 'Oral PrEP',
        '019': 'Termination of Pregnancy - 1st Trimester',
        '020': 'Termination of Pregnancy - 2nd Trimester',
        '021': 'AYFS Accredited',
        '022': 'CCMDD Pick Up Point',
    }

    def get(self, request, service_id):
        location = request.query_params.get('location', None)
        if location is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        lat, lon = location.split(',')
        url = settings.MAPIT_LOCATION_URL + '{},{}?type=MN'.format(lon, lat)
        req = requests.get(url)
        geo = req.json()
        if geo:
            for _, value in geo.items():
                mdb = value['codes']['MDB']
                municipality_name = value['name']
            query = HealthFacilities\
                .objects\
                .filter(service__contains={self.services[service_id]: 'Yes'},
                        geo_levels__contains=[mdb])
            serialize = serializers.HealthFacilitySerializer(query, many=True)
            return Response({
                'data': serialize.data,
                'municipality': municipality_name,
                'municipality_code': mdb,
                'service': self.services[service_id]
            })
        else:
            return Response(
                {
                    'error': 'No data for location'
                },
                status=status.HTTP_404_NOT_FOUND)


class GeographyView(APIView):
    """
    Return a List of all the districts in the country
    """

    def get(self, request):
        query = Geography.objects.filter(parent_level='province', version=2016)
        serialize = serializers.GeographySerializer(query, many=True)

        return Response({'data': serialize.data})


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
