from django.urls import path

from core.sh.views.ajax_views import ajax_load_dependency, ajax_load_edifices, ajax_load_employee, ajax_load_loc, ajax_load_location, ajax_load_model, ajax_load_office, ajax_load_switch_port, ajax_load_wall_port


app_name = 'sh'

urlpatterns = [

  # Ajax Routes
  path('ajax/load_location/', ajax_load_location, name="device_search_location"),
  path('ajax/load_dependency/', ajax_load_dependency, name="device_load_dependency"),
  path('ajax/load_edifices/', ajax_load_edifices, name="device_load_edifice"),
  path('ajax/load_loc/', ajax_load_loc, name="device_load_loc"),
  path('ajax/load_office/', ajax_load_office, name="device_load_office"),
  path('ajax/load_wall_port/', ajax_load_wall_port, name="device_load_wall_port"),
  path('ajax/load_switch_port/', ajax_load_switch_port, name="device_load_switch_port"),
  path('ajax/load_employee/', ajax_load_employee, name="device_load_employee"),
  path('ajax/load_model/', ajax_load_model, name="device_load_model"),

]