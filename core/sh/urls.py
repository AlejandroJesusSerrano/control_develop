from django.urls import include, path

urlpatterns = []

from .url_modules.brands_urls import urlpatterns as brands_url
from .url_modules.connection_type_url import urlpatterns as connection_type_url
from .url_modules.dahsboard_urls import urlpatterns as dashboard_url
from .url_modules.dependency_url import urlpatterns as dependency_url
from .url_modules.dev_status_url import urlpatterns as dev_status_url
from .url_modules.dev_type_url import urlpatterns as dev_type_url
from .url_modules.dev_model_url import urlpatterns as dev_model_url
from .url_modules.device_url import urlpatterns as device_url
from .url_modules.edifice_url import urlpatterns as edifice_url
from .url_modules.employee_url import urlpatterns as employee_url
from .url_modules.employee_status_url import urlpatterns as employee_status_url
from .url_modules.location_url import urlpatterns as location_url
from .url_modules.move_type_url import urlpatterns as move_type_url
from .url_modules.movements_url import urlpatterns as movements_url
from .url_modules.office_url import urlpatterns as office_url
from .url_modules.office_loc_url import urlpatterns as office_loc_url
from .url_modules.patch_port_url import urlpatterns as patch_port_url
from .url_modules.patchera_url import urlpatterns as patchera_url
from .url_modules.province_url import urlpatterns as province_url
from .url_modules.rack_url import urlpatterns as rack_url
from .url_modules.suply_url import urlpatterns as suply_url
from .url_modules.suply_type_url import urlpatterns as suply_type_url
from .url_modules.switch_url import urlpatterns as switch_url
from .url_modules.switch_port_url import urlpatterns as switch_port_url
from .url_modules.techs_url import urlpatterns as techs_url
from .url_modules.wall_port_url import urlpatterns as wall_port_url
from .url_modules.ajax_urls import urlpatterns as ajax_url

urlpatterns += brands_url
urlpatterns += connection_type_url
urlpatterns += dashboard_url
urlpatterns += dependency_url
urlpatterns += dev_status_url
urlpatterns += dev_type_url
urlpatterns += dev_model_url
urlpatterns += device_url
urlpatterns += edifice_url
urlpatterns += employee_url
urlpatterns += employee_status_url
urlpatterns += location_url
urlpatterns += move_type_url
urlpatterns += movements_url
urlpatterns += office_url
urlpatterns += office_loc_url
urlpatterns += patch_port_url
urlpatterns += patchera_url
urlpatterns += province_url
urlpatterns += rack_url
urlpatterns += suply_url
urlpatterns += suply_type_url
urlpatterns += switch_url
urlpatterns += switch_port_url
urlpatterns += techs_url
urlpatterns += wall_port_url
urlpatterns += ajax_url
