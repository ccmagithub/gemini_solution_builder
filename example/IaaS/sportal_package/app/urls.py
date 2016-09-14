from django.conf.urls import url
from sportal.service import views as service_views
import views as iaas_views

urlpatterns = [
    url(r'^$', service_views.common_service_index, name='iaas_index'),
    url(r'^create_site/$', iaas_views.create_site, name='iaas_create_site'),
    url(r'^delete_site/$', service_views.common_service_delete_site,
        name='iaas_delete_site'),
    url(r'^start_site/$', service_views.common_service_start_site,
        name='iaas_start_site'),
    url(r'^stop_site/$', service_views.common_service_stop_site,
        name='iaas_stop_site'),
    url(r'^detail/(?P<site_id>\d+)/$', iaas_views.detail_view,
        name='iaas_detail'),
]
