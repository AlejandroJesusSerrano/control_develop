from django.urls import path

from core.sh.views.switch_port.views import Switch_PortCreateView, Switch_PortDeleteView, Switch_PortListView, Switch_PortUpdateView

app_name = 'sh'

urlpatterns = [

  path('switch_port/list/', Switch_PortListView.as_view(), name='switch_port_list'),
  path('switch_port/add/', Switch_PortCreateView.as_view(), name='switch_port_add'),
  path('switch_port/edit/<int:pk>/', Switch_PortUpdateView.as_view(), name='switch_port_edit'),
  path('switch_port/delete/<int:pk>/', Switch_PortDeleteView.as_view(), name='switch_port_delete')

]