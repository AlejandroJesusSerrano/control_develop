from django.urls import path

from core.sh.views.device.views import DeviceCreateView, DeviceDeleteView, DeviceListView, DeviceUpdateView, ajax_device_load_dependency, ajax_device_load_edifices, ajax_device_load_employee, ajax_device_load_loc, ajax_device_load_model, ajax_device_load_office, ajax_device_load_switch_port, ajax_device_load_wall_port, ajax_device_search_location

app_name = 'sh'

urlpatterns = [

  # Devices
  path('device/list/', DeviceListView.as_view(), name='device_list'),
  path('device/add/', DeviceCreateView.as_view(), name='device_add'),
  path('device/edit/<int:pk>/', DeviceUpdateView.as_view(), name='device_edit'),
  path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),
  # Ajax Routes
  path('ajax/search_device_location/', ajax_device_search_location, name="device_search_location"),
  path('ajax/load_dependency/', ajax_device_load_dependency, name="device_load_dependency"),
  path('ajax/load_edifices/', ajax_device_load_edifices, name="device_load_edifice"),
  path('ajax/load_loc/', ajax_device_load_loc, name="device_load_loc"),
  path('ajax/load_office/', ajax_device_load_office, name="device_load_office"),
  path('ajax/load_wall_port/', ajax_device_load_wall_port, name="device_load_wall_port"),
  path('ajax/load_switch_port/', ajax_device_load_switch_port, name="device_load_switch_port"),
  path('ajax/load_employee/', ajax_device_load_employee, name="device_load_employee"),
  path('ajax/load_model/', ajax_device_load_model, name="device_load_model"),

]