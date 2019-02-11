from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from api import views as api
from . import views

urlpatterns = [
    url(r'^', include('wazimap.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^activity/', include('partner.urls')),
    url(r'^point/data/(?P<geo_code>\w+)/(?P<dataset>\w+)$',
        views.show_facilities,
        name='show_facilities'),
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
        name='service_geography')
]

#urlpatterns += urls.urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
