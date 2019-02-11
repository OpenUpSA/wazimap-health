from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<geo_name>[\w -| ]+)/organisation/(?P<org_slug>[\w-]+)$',
        views.partner_profile,
        name='partner_profile'),
]
