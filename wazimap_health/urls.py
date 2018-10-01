from django.conf.urls import url, patterns, include
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from .admin import admin_site
from wazimap import urls

from api import views as api
from api import schema

urlpatterns = patterns(
    '',
    url(
        '^docs/',
        include_docs_urls(
            title='Health Facility API',
            public=False,
            patterns=[
                url(r'^api/point/v1/services$',
                    api.HealthServiceView.as_view(),
                    name='services'),
                url(r'^api/point/v1/services/(?P<service_id>\d+)$',
                    api.ServiceView.as_view(),
                    name='geo_service'),
                # url(r'^api/point/v1/geography$',
                #     api.GeographyView.as_view(),
                #     name='service_geography'),
                # url(r'^api/point/v1/geography/(?P<district_id>\w+)')
            ])),
    url(r'^api/point/v1/health/facilities$',
        api.HealthView.as_view(),
        name='health_facility'),
    url('^api/point/v1/education/higher/facilities$',
        api.HigherEducationView.as_view(),
        name='higher_education'),
    url(r'api/point/v1/education/basic/facilities$',
        api.BasicEducationView.as_view(),
        name='basic_education'),
    url(r'^api/point/v1/facilities',
        api.FacilityView.as_view(),
        name='facility'),
    url(r'^api/point/v1/services$',
        api.HealthServiceView.as_view(),
        name='services'),
    url(r'^api/point/v1/services/(?P<service_id>\d+)$',
        api.ServiceView.as_view(),
        name='geo_service'),
    url(r'^api/point/v1/geography$',
        api.GeographyView.as_view(),
        name='service_geography'),
    url(r'^admin/', include(admin_site.urls)))

urlpatterns += urls.urlpatterns
