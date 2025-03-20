from django.urls import path

from core.sh.views.device.views import DeviceCreateView, DeviceDeleteView, DeviceDetailsView, DeviceListView, DeviceUpdateView

app_name = 'sh'

urlpatterns = [

  # Devices
  path('device/list/', DeviceListView.as_view(), name='device_list'),
  path('device/add/', DeviceCreateView.as_view(), name='device_add'),
  path('device/edit/<int:pk>/', DeviceUpdateView.as_view(), name='device_edit'),
  path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),
  path('device/details/<int:pk>/', DeviceDetailsView.as_view(), name='device_details'),

]