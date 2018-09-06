from django.conf.urls import url, patterns, include
from django.contrib import admin
from wazimap import urls

# from api import views

urlpatterns = patterns('',
                       # url(r'api/point/v1/facilities$',
                       #     views.FacilityView.as_view(),
                       #     name='health_facility'),
                       url(r'^admin/', include(admin.site.urls)))

urlpatterns += urls.urlpatterns
