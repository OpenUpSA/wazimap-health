from django.conf.urls import url, patterns, include
from django.contrib import admin
from .admin import admin_site
from wazimap import urls

from api import views as api

urlpatterns = patterns('',
                       url(r'^api/point/v1/health/facilities$',
                           api.HealthView.as_view(),
                           name='health_facility'),
                       url('^api/point/v1/education/facilities$',
                           api.HigherEducationView.as_view(),
                           name='higher_education'),
                       url(r'^api/point/v1/facilities',
                           api.FacilityView.as_view(),
                           name='facility'),
                       url(r'^admin/', include(admin_site.urls)))

urlpatterns += urls.urlpatterns
