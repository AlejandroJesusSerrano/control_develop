from django.urls import path
from core.sh.views.ajax_views import (
    ajax_load_brand, ajax_load_dev_type, ajax_load_employee, ajax_load_location, ajax_load_dependency, ajax_load_edifices,
    ajax_load_loc, ajax_load_office, ajax_load_rack, ajax_load_switch,
    ajax_load_patchera, ajax_load_patch_ports, ajax_load_model, ajax_load_switch_port, ajax_load_wall_port
)

urlpatterns = [
    path('ajax/load_location/', ajax_load_location, name='ajax_load_location'),
    path('ajax/load_dependency/', ajax_load_dependency, name='ajax_load_dependency'),
    path('ajax/load_edifices/', ajax_load_edifices, name='ajax_load_edifices'),
    path('ajax/load_loc/', ajax_load_loc, name='ajax_load_loc'),
    path('ajax/load_office/', ajax_load_office, name='ajax_load_office'),
    path('ajax/load_brand/', ajax_load_brand, name='ajax_load_brand'),
    path('ajax/load_dev_type/', ajax_load_dev_type, name='ajax_load_dev_type'),
    path('ajax/load_rack/', ajax_load_rack, name='ajax_load_rack'),
    path('ajax/load_switch/', ajax_load_switch, name='ajax_load_switch'),
    path('ajax/load_patchera/', ajax_load_patchera, name='ajax_load_patchera'),
    path('ajax/load_patch_ports/', ajax_load_patch_ports, name='ajax_load_patch_ports'),
    path('ajax/load_model/', ajax_load_model, name='ajax_load_model'),
    path('ajax/load_wall_port/', ajax_load_wall_port, name = 'ajax_load_wall_port'),
    path('ajax/load_employee/', ajax_load_employee, name = 'ajax_load_employee' ),
    path('ajax/load_switch_port/', ajax_load_switch_port, name = 'ajax_load_switch_port')
]
