from django.conf.urls import url, patterns, include
from django.contrib import admin
from .admin import admin_site
from wazimap import urls

from api import views as api

urlpatterns = patterns('',
                       url(r'^api/point/v1/facilities$',
                           api.HealthFacilityView.as_view(),
                           name='health_facility'),
                       #url(r'^api/point/v1/facilities/(?P<geo_code>\w+)/services$'),
                       url(r'^admin/', include(admin_site.urls)))

urlpatterns += urls.urlpatterns
