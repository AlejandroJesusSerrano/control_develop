from django.urls import path

from core.sh.views.patch_port import views
from core.sh.views.patch_port.views import Patch_PortCreateView, Patch_PortDeleteView, Patch_PortListView, Patch_PortUpadateView

app_name = 'sh'

urlpatterns = [

  path('patch_port/list/', Patch_PortListView.as_view(), name='patch_port_list'),
  path('patch_port/add/', Patch_PortCreateView.as_view(), name='patch_port_add'),
  path('patch_port/edit/<int:pk>/', Patch_PortUpadateView.as_view(), name='patch_port_edit'),
  path('patch_port/delete/<int:pk>/', Patch_PortDeleteView.as_view(), name='patch_port_delete'),
  # filter by office
  path('get_patch_ports_by_rack/', views.get_patch_ports_by_rack, name='get_patch_ports_by_rack'),
  path('get_patch_ports_by_office/', views.get_patch_ports_by_office, name='get_patch_ports_by_office')
]