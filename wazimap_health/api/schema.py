import coreapi
from rest_framework import schemas


class CustomSchemaGenerator(schemas.SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        super(CustomSchemaGenerator, self).get_schema(*args, **kwargs)
        return coreapi.Document(
            title=self.title,
            description=
            'API for view health facilitys and the services they offer',
            url=self.url,
            content={
                'Health Services':
                coreapi.Link(
                    url='/api/point/v1/services',
                    action='get',
                    description='Return a list of all the health services'),
                'Services':
                coreapi.Link(
                    url='/api/point/v1/services/{service_id}',
                    action='get',
                    fields=[
                        coreapi.Field(
                            name='service_id',
                            required=True,
                            location='path',
                            description='Unique number for a health service'),
                        coreapi.Field(
                            name='location',
                            required=True,
                            location='query',
                            description=
                            'location expressed in as lat,long coordinates'),
                    ],
                    description=
                    'Return a list of facility that provide that service within that location'
                ),
            })
