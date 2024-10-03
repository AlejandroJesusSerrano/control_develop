from django.urls import include, path

urlpatterns = []


from .url_modules.brands_urls import urlpatterns as brands_urls
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

urlpatterns += brands_urls
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



# from django.urls import include, path

# from core.sh.views.connection_type.views import Connection_TypeCreateView, Connection_TypeDeleteView, Connection_TypeListView, Connection_TypeUpadateView
# from core.sh.views.device.views import DeviceCreateView, DeviceDeleteView, DeviceListView, DeviceUpdateView
# from core.sh.views.office.views import OfficeCreateView, OfficeListView, OfficeDeleteView, OfficeUpdateView, ajax_load_dependency, ajax_load_edifices, ajax_load_loc, ajax_office_search_location
# from core.sh.views.office_loc.views import Office_Loc_ListView, Office_Loc_CreateView, Office_Loc_UpdateView, Office_Loc_DeleteView, ajax_office_loc_search_edifice, ajax_office_loc_search_location
# from core.sh.views.patch_port.views import Patch_PortCreateView, Patch_PortDeleteView, Patch_PortListView, Patch_PortUpadateView
# from core.sh.views.patchera.views import PatcheraCreateView, PatcheraDeleteView, PatcheraListView, PatcheraUpadateView
# from core.sh.views.province.views import ProvinceDeleteView, ProvinceListView, ProvinceCreateView, ProvinceUpdateView
# from core.sh.views.location.views import LocationListView, LocationCreateView, LocationUpadateView, LocationDeleteView
# from core.sh.views.edifice.views import EdificeListView, EdificeCreateView, EdificeUpdateView, EdificeDeleteView, ajax_edifice_search_location
# from core.sh.views.dependency.views import DependencyListView, DependencyCreateView, DependencyDeleteView, DependencyUpdateView, ajax_dependency_search_edifice, ajax_dependency_search_location
# from core.sh.views.brands.views import BrandListView, BrandCreateView, BrandUpadateView, BrandDeleteView
# from core.sh.views.dev_type.views import Dev_TypeListView, Dev_TypeCreateView, Dev_TypeUpadateView, Dev_TypeDeleteView
# from core.sh.views.dev_status.views import Dev_StatusCreateView, Dev_StatusDeleteView, Dev_StatusUpadateView, DevStatusListView
# from core.sh.views.dev_model.views import Dev_ModelsCreateView, Dev_ModelsListView, Dev_ModelsUpadateView, Dev_ModelsDeleteView
# from core.sh.views.employee_status.views import EmployeeStatusListView, EmployeeStatusCreateView, EmnployeeStatusUpdateView, EmployeeStatusDeleteView
# from core.sh.views.employee.views import EmployeeListView, EmployeeCreateView, EmployeeUpadateView, EmployeeDeleteView
# from core.sh.views.rack.views import RackCreateView, RackDeleteView, RackListView, RackUpadateView
# from core.sh.views.suply.views import SuplyCreateView, SuplyDeleteView, SuplyListView, SuplyUpadateView
# from core.sh.views.suply_type.views import SuplyTypeCreateView, SuplyTypeDeleteView, SuplyTypeListView, SuplyTypeUpadateView
# from core.sh.views.switch import views as switch_views
# from core.sh.views.switch_port.views import Switch_PortCreateView, Switch_PortDeleteView, Switch_PortListView, Switch_PortUpadateView
# from core.sh.views.tehcs.views import TechsDeleteView, TechsListView, TechsCreateView, TechsUpadateView
# from core.sh.views.dashboard.views import DashboardView
# from core.sh.views.wall_port.views import WallPortCreateView, WallPortDeleteView, WallPortListView, WallPortUpdateView


# app_name = 'sh'

# urlpatterns = [
#   # Home
#   path('dashboard/', DashboardView.as_view(), name='dashboard'),
  # Provinces
  # path('prov/list/', ProvinceListView.as_view(), name='province_list'),
  # path('prov/add/', ProvinceCreateView.as_view(), name='province_add' ),
  # path('prov/edit/<int:pk>/', ProvinceUpdateView.as_view(), name='province_edit' ),
  # path('prov/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete' ),
  # # Location
  # path('location/list/', LocationListView.as_view(), name='location_list'),
  # path('location/add/', LocationCreateView.as_view(), name='location_add'),
  # path('location/edit/<int:pk>/', LocationUpadateView.as_view(), name='location_edit'),
  # path('location/delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),

  # # Edifice
  # path('edifice/list/', EdificeListView.as_view(), name='edifice_list'),
  # path('edifice/add/', EdificeCreateView.as_view(), name='edifice_add'),
  # path('edifice/edit/<int:pk>/', EdificeUpdateView.as_view(), name='edifice_edit'),
  # path('edifice/delete/<int:pk>/', EdificeDeleteView.as_view(), name='edifice_delete'),
  # # Edifice Ajax Route
  # path('ajax/search_edifice_location/', ajax_edifice_search_location, name='ajax_search_edifice_location'),

  # # Dependency
  # path('dependency/list/', DependencyListView.as_view(), name='dependency_list'),
  # path('dependency/add/', DependencyCreateView.as_view(), name='dependency_add'),
  # path('dependency/edit/<int:pk>/', DependencyUpdateView.as_view(), name='dependency_edit'),
  # path('dependency/delete/<int:pk>/', DependencyDeleteView.as_view(), name='dependency_delete'),
  # # Dependency Ajax Route
  # path('ajax/search_dependency_location/', ajax_dependency_search_location, name='ajax_search_dependency_location'),
  # path('ajax/search_dependency_edifice/', ajax_dependency_search_edifice, name='ajax_search_dependency_edifice'),

  # # Office_Loc
  # path('office_loc/list/', Office_Loc_ListView.as_view(), name='office_loc_list'),
  # path('office_loc/add/', Office_Loc_CreateView.as_view(), name='office_loc_add'),
  # path('office_loc/edit/<int:pk>/', Office_Loc_UpdateView.as_view(), name='office_loc_edit'),
  # path('office_loc/delete/<int:pk>/', Office_Loc_DeleteView.as_view(), name='office_loc_delete'),
  # # Office Loc Ajax Routes
  # path('ajax/search_office_loc_location/', ajax_office_loc_search_location, name='ajax_search_office_loc_location'),
  # path('ajax/search_office_loc_edifice/', ajax_office_loc_search_edifice, name='ajax_office_loc_search_edifice'),

  # # Office
  # path('office/list/', OfficeListView.as_view(), name='office_list'),
  # path('office/add/', OfficeCreateView.as_view(), name='office_add'),
  # path('office/edit/<int:pk>/', OfficeUpdateView.as_view(), name='office_edit'),
  # path('office/delete/<int:pk>/', OfficeDeleteView.as_view(), name='office_delete'),
  # # Office Ajax Routes
  # path('ajax/search_office_location/', ajax_office_search_location, name='ajax_search_office_location'),
  # path('ajax/load_dependency/', ajax_load_dependency, name='ajax_load_dependency'),
  # path('ajax/load_edifice/', ajax_load_edifices, name='ajax_load_edifice'),
  # path('ajax/load_loc/', ajax_load_loc, name='ajax_load_loc'),

  # # Connection Type
  # path('connection_type/list/', Connection_TypeListView.as_view(), name='connection_type_list'),
  # path('connection_type/add/', Connection_TypeCreateView.as_view(), name='connection_type_add'),
  # path('connection_type/edit/<int:pk>/', Connection_TypeUpadateView.as_view(), name='connection_type_edit'),
  # path('connection_type/delete/<int:pk>/', Connection_TypeDeleteView.as_view(), name='connection_type_delete'),
  # # Rack
  # path('rack/list/', RackListView.as_view(), name='rack_list'),
  # path('rack/add/', RackCreateView.as_view(), name='rack_add'),
  # path('rack/edit/<int:pk>/', RackUpadateView.as_view(), name='rack_edit'),
  # path('rack/delete/<int:pk>/', RackDeleteView.as_view(), name='rack_delete'),

  # # Switchs
  # path('switch/list/', switch_views.SwitchListView.as_view(), name='switch_list'),
  # path('switch/add/', switch_views.SwitchCreateView.as_view(), name='switch_add'),
  # path('switch/edit/<int:pk>/', switch_views.SwitchUpdateView.as_view(), name='switch_edit'),
  # path('switch/delete/<int:pk>/', switch_views.SwitchDeleteView.as_view(), name='switch_delete'),
  # # Ajax Switch Routes
  # path('ajax/search_switch_brand/', switch_views.ajax_switch_search_brand, name='ajax_search_switch_brand'),
  # path('ajax/search_switch_model/', switch_views.ajax_switch_search_model, name='ajax_search_switch_model'),
  # path('ajax/search_switch_location/', switch_views.ajax_switch_search_location, name='ajax_search_switch_location'),
  # path('ajax/search_switch_edifice/', switch_views.ajax_switch_search_edifice, name='ajax_search_switch_edifice'),
  # path('ajax/search_switch_dependency/', switch_views.ajax_switch_search_dependency, name='ajax_search_switch_dependency'),
  # path('ajax/search_switch_office/', switch_views.ajax_switch_search_office, name='ajax_search_switch_office'),

  # # Switch Ports
  # path('switch_port/list/', Switch_PortListView.as_view(), name='switch_port_list'),
  # path('switch_port/add/', Switch_PortCreateView.as_view(), name='switch_port_add'),
  # path('switch_port/edit/<int:pk>/', Switch_PortUpadateView.as_view(), name='switch_port_edit'),
  # path('switch_port/delete/<int:pk>/', Switch_PortDeleteView.as_view(), name='switch_port_delete'),
  # # Patchera
  # path('patchera/list/', PatcheraListView.as_view(), name='patchera_list'),
  # path('patchera/add/', PatcheraCreateView.as_view(), name='patchera_add'),
  # path('patchera/edit/<int:pk>/', PatcheraUpadateView.as_view(), name='patchera_edit'),
  # path('patchera/delete/<int:pk>/', PatcheraDeleteView.as_view(), name='patchera_delete'),
  # # Patch Ports
  # path('patch_port/list/', Patch_PortListView.as_view(), name='patch_port_list'),
  # path('patch_port/add/', Patch_PortCreateView.as_view(), name='patch_port_add'),
  # path('patch_port/edit/<int:pk>/', Patch_PortUpadateView.as_view(), name='patch_port_edit'),
  # path('patch_port/delete/<int:pk>/', Patch_PortDeleteView.as_view(), name='patch_port_delete'),
  # # Wall Ports
  # path('wall_port/list/', WallPortListView.as_view(), name='wall_port_list'),
  # path('wall_port/add/', WallPortCreateView.as_view(), name='wall_port_add'),
  # path('wall_port/edit/<int:pk>/', WallPortUpdateView.as_view(), name='wall_port_edit'),
  # path('wall_port/delete/<int:pk>/', WallPortDeleteView.as_view(), name='wall_port_delete'),

  # DEVICES
  # # Brands
  # path('brand/list/', BrandListView.as_view(), name='brand_list'),
  # path('brand/add/', BrandCreateView.as_view(), name='brand_add'),
  # path('brand/edit/<int:pk>/', BrandUpadateView.as_view(), name='brand_edit'),
  # path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
  # # Dev_Type
  # path('dev_type/list/', Dev_TypeListView.as_view(), name='dev_type_list'),
  # path('dev_type/add/', Dev_TypeCreateView.as_view(), name='dev_type_add'),
  # path('dev_type/edit/<int:pk>/', Dev_TypeUpadateView.as_view(), name='dev_type_edit'),
  # path('dev_type/delete/<int:pk>/', Dev_TypeDeleteView.as_view(), name='dev_type_delete'),
  # #Dev_Status
  # path('dev_status/list/', DevStatusListView.as_view(), name='dev_status_list'),
  # path('dev_status/add/', Dev_StatusCreateView.as_view(), name='dev_status_add'),
  # path('dev_status/edit/<int:pk>/', Dev_StatusUpadateView.as_view(), name='dev_status_edit'),
  # path('dev_status/delete/<int:pk>/', Dev_StatusDeleteView.as_view(), name='dev_status_delete'),
  # # Models
  # path('dev_model/list/', Dev_ModelsListView.as_view(), name='dev_model_list'),
  # path('dev_model/add/', Dev_ModelsCreateView.as_view(), name='dev_model_add'),
  # path('dev_model/edit/<int:pk>/', Dev_ModelsUpadateView.as_view(), name='dev_model_edit'),
  # path('dev_model/delete/<int:pk>/', Dev_ModelsDeleteView.as_view(), name='dev_model_delete'),
  # # Devices
  # path('device/list/', DeviceListView.as_view(), name='device_list'),
  # path('device/add/', DeviceCreateView.as_view(), name='device_add'),
  # path('device/edit/<int:pk>/', DeviceUpdateView.as_view(), name='device_edit'),
  # path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),

  # # DINAMIC TABLES
  # # Employee_Status
  # path('employee_status/list/', EmployeeStatusListView.as_view(), name='employee_status_list'),
  # path('employee_status/add/', EmployeeStatusCreateView.as_view(), name='employee_status_add'),
  # path('employee_status/edit/<int:pk>/', EmnployeeStatusUpdateView.as_view(), name='employee_status_edit'),
  # path('employee_status/delete/<int:pk>/', EmployeeStatusDeleteView.as_view(), name='employee_status_delete'),
  # # Employee
  # path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
  # path('employee/add/', EmployeeCreateView.as_view(), name='employee_add'),
  # path('employee/edit/<int:pk>/', EmployeeUpadateView.as_view(), name='employee_edit'),
  # path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
  # # Techs
  # path('techs/list/', TechsListView.as_view(), name='techs_list'),
  # path('techs/add/', TechsCreateView.as_view(), name='techs_add'),
  # path('techs/edit/<int:pk>/', TechsUpadateView.as_view(), name='techs_edit'),
  # path('techs/delete/<int:pk>/', TechsDeleteView.as_view(), name='techs_delete'),

  # DEVICES & SUPLYES
  # # Suply Type
  # path('suply_type/list/', SuplyTypeListView.as_view(), name='suply_type_list'),
  # path('suply_type/add/', SuplyTypeCreateView.as_view(), name='suply_type_add'),
  # path('suply_type/edit/<int:pk>/', SuplyTypeUpadateView.as_view(), name='suply_type_edit'),
  # path('suply_type/delete/<int:pk>/', SuplyTypeDeleteView.as_view(), name='suply_type_delete'),
  # # Suply
  # path('suply/list/', SuplyListView.as_view(), name='suply_list'),
  # path('suply/add/', SuplyCreateView.as_view(), name='suply_add'),
  # path('suply/edit/<int:pk>/', SuplyUpadateView.as_view(), name='suply_edit'),
  # path('suply/delete/<int:pk>/', SuplyDeleteView.as_view(), name='suply_delete'),
# ]