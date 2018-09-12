from django.conf.urls import url, patterns, include
from django.contrib import admin
from wazimap import urls

from api import views as api
from . import views

urlpatterns = patterns('',
                       url(r'api/point/v1/facilities$',
                           api.PublicFacilityView.as_view(),
                           name='health_facility'),
                       url(r'api/point/v1/facilities/(?P<code>\w+)/services$',
                           api.PublicServicesView.as_view(),
                           name='health_services'),
                       url(r'api/point/v1/pharmacies$',
                           api.PharmacyView.as_view(),
                           name='private_pharmacy'),
                       url(r'point/profile$', views.point_detail),
                       url(r'^admin/', include(admin.site.urls)))

urlpatterns += urls.urlpatterns
