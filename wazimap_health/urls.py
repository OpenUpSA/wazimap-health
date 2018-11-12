from django.conf.urls import url, patterns, include
from rest_framework.documentation import include_docs_urls
from django.conf.urls.static import static
from django.conf import settings
from .admin import admin_site
from wazimap import urls
from api import views as api
from . import views

urlpatterns = patterns(
    '',
    url(
        '^docs/',
        include_docs_urls(
            title='Health Facility API',
            public=False,
            #generator_class=schema.CustomSchemaGenerator,
            patterns=[
                url(r'^api/point/v1/services$',
                    api.HealthServiceView.as_view(),
                    name='services'),
                url(r'^api/point/v1/services/(?P<service_id>\d+)$',
                    api.ServiceView.as_view(),
                    name='geo_service'),
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
    url(r'^admin/', include(admin_site.urls)),
    url(r'^activity/(?P<geo_name>[\w -| ]+)/organisation/(?P<org_slug>[\w-]+)$',
        views.organisation_profile,
        name='organisation_profile'))

urlpatterns += urls.urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
