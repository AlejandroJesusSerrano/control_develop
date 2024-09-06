from django.urls import path

from core.sh.views.connection_type.views import Connection_TypeCreateView, Connection_TypeDeleteView, Connection_TypeListView, Connection_TypeUpadateView
from core.sh.views.device.views import DeviceCreateView, DeviceDeleteView, DeviceListView, DeviceUpdateView
from core.sh.views.office.views import OfficeCreateView, OfficeListView, OfficeUpadateView, OfficeDeleteView
from core.sh.views.office_loc.views import OfficeLocListView
# , OfficeLocCreateView, OfficeLocUpadateView, OfficeLocDeleteView
from core.sh.views.patch_port.views import Patch_PortCreateView, Patch_PortDeleteView, Patch_PortListView, Patch_PortUpadateView
from core.sh.views.patchera.views import PatcheraCreateView, PatcheraDeleteView, PatcheraListView, PatcheraUpadateView
from core.sh.views.province.views import ProvinceDeleteView, ProvinceFormView, ProvinceListView, ProvinceCreateView, ProvinceUpdateView
from core.sh.views.location.views import LocationListView, LocationCreateView, LocationUpadateView, LocationDeleteView
from core.sh.views.edifice.views import EdificeListView, EdificeCreateView, EdificeUpadateView, EdificeDeleteView
from core.sh.views.dependency.views import DependencyListView, DependencyCreateView, DependencyUpadateView, DependencyDeleteView
from core.sh.views.brands.views import BrandListView, BrandCreateView, BrandUpadateView, BrandDeleteView
from core.sh.views.dev_type.views import Dev_TypeListView, Dev_TypeCreateView, Dev_TypeUpadateView, Dev_TypeDeleteView
from core.sh.views.dev_status.views import Dev_StatusCreateView, Dev_StatusDeleteView, Dev_StatusUpadateView, DevStatusListView
from core.sh.views.dev_model.views import Dev_ModelsCreateView, Dev_ModelsListView, Dev_ModelsUpadateView, Dev_ModelsDeleteView
from core.sh.views.employee_status.views import EmployeeStatusListView, EmployeeStatusCreateView, EmnployeeStatusUpdateView, EmployeeStatusDeleteView
from core.sh.views.employee.views import EmployeeListView, EmployeeCreateView, EmployeeUpadateView, EmployeeDeleteView
from core.sh.views.rack.views import RackCreateView, RackDeleteView, RackListView, RackUpadateView
from core.sh.views.suply.views import SuplyCreateView, SuplyDeleteView, SuplyListView, SuplyUpadateView
from core.sh.views.suply_type.views import SuplyTypeCreateView, SuplyTypeDeleteView, SuplyTypeListView, SuplyTypeUpadateView
from core.sh.views.switch.views import SwitchCreateView, SwitchDeleteView, SwitchListView, SwitchUpadateView
from core.sh.views.switch_port.views import Switch_PortCreateView, Switch_PortDeleteView, Switch_PortListView, Switch_PortUpadateView
from core.sh.views.tehcs.views import TechsDeleteView, TechsListView, TechsCreateView, TechsUpadateView
from core.sh.views.dashboard.views import DashboardView
from core.sh.views.wall_port.views import WallPortCreateView, WallPortDeleteView, WallPortListView, WallPortUpdateView


app_name = 'sh'

urlpatterns = [
  #* Home
  path('dashboard/', DashboardView.as_view(), name='dashboard'),

  # Provinces
  path('prov/list/', ProvinceListView.as_view(), name='province_list'),
  path('prov/add/', ProvinceCreateView.as_view(), name='province_add' ),
  path('prov/edit/<int:pk>/', ProvinceUpdateView.as_view(), name='province_edit' ),
  path('prov/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete' ),
  path('prov/form/', ProvinceFormView.as_view(), name = 'p_form'),
  # Location
  path('location/list/', LocationListView.as_view(), name='location_list'),
  path('location/add/', LocationCreateView.as_view(), name='location_add'),
  path('location/edit/<int:pk>/', LocationUpadateView.as_view(), name='location_edit'),
  path('location/delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),
  # Edifice
  path('edifice/list/', EdificeListView.as_view(), name='edifice_list'),
  path('edifice/add/', EdificeCreateView.as_view(), name='edifice_add'),
  path('edifice/edit/<int:pk>/', EdificeUpadateView.as_view(), name='edifice_edit'),
  path('edifice/delete/<int:pk>/', EdificeDeleteView.as_view(), name='edifice_delete'),
  # Dependency
  path('dependency/list/', DependencyListView.as_view(), name='dependency_list'),
  path('dependency/add/', DependencyCreateView.as_view(), name='dependency_add'),
  path('dependency/edit/<int:pk>/', DependencyUpadateView.as_view(), name='dependency_edit'),
  path('dependency/delete/<int:pk>/', DependencyDeleteView.as_view(), name='dependency_delete'),
  # Office_Loc
  path('office_loc/list/', OfficeLocListView.as_view(), name='office_loc_list'),
  # path('office_loc/add/', OfficeLocCreateView.as_view(), name='office_loc_add'),
  # path('office_loc/edit/<int:pk>/', OfficeLocUpadateView.as_view(), name='office_loc_edit'),
  # path('office_loc/delete/<int:pk>/', OfficeLocDeleteView.as_view(), name='office_loc_delete'),
  # Office
  path('office/list/', OfficeListView.as_view(), name='office_list'),
  path('office/add/', OfficeCreateView.as_view(), name='office_add'),
  path('office/edit/<int:pk>/', OfficeUpadateView.as_view(), name='office_edit'),
  path('office/delete/<int:pk>/', OfficeDeleteView.as_view(), name='office_delete'),
  # Connection Type
  path('connection_type/list/', Connection_TypeListView.as_view(), name='connection_type_list'),
  path('connection_type/add/', Connection_TypeCreateView.as_view(), name='connection_type_add'),
  path('connection_type/edit/<int:pk>/', Connection_TypeUpadateView.as_view(), name='connection_type_edit'),
  path('connection_type/delete/<int:pk>/', Connection_TypeDeleteView.as_view(), name='connection_type_delete'),
  # Rack
  path('rack/list/', RackListView.as_view(), name='rack_list'),
  path('rack/add/', RackCreateView.as_view(), name='rack_add'),
  path('rack/edit/<int:pk>/', RackUpadateView.as_view(), name='rack_edit'),
  path('rack/delete/<int:pk>/', RackDeleteView.as_view(), name='rack_delete'),
  # Switchs
  path('switch/list/', SwitchListView.as_view(), name='switch_list'),
  path('switch/add/', SwitchCreateView.as_view(), name='switch_add'),
  path('switch/edit/<int:pk>/', SwitchUpadateView.as_view(), name='switch_edit'),
  path('switch/delete/<int:pk>/', SwitchDeleteView.as_view(), name='switch_delete'),
  #Switch Ports
  path('switch_port/list/', Switch_PortListView.as_view(), name='switch_port_list'),
  path('switch_port/add/', Switch_PortCreateView.as_view(), name='switch_port_add'),
  path('switch_port/edit/<int:pk>/', Switch_PortUpadateView.as_view(), name='switch_port_edit'),
  path('switch_port/delete/<int:pk>/', Switch_PortDeleteView.as_view(), name='switch_port_delete'),
  # Patchera
  path('patchera/list/', PatcheraListView.as_view(), name='patchera_list'),
  path('patchera/add/', PatcheraCreateView.as_view(), name='patchera_add'),
  path('patchera/edit/<int:pk>/', PatcheraUpadateView.as_view(), name='patchera_edit'),
  path('patchera/delete/<int:pk>/', PatcheraDeleteView.as_view(), name='patchera_delete'),
  # Patch Ports
  path('patch_port/list/', Patch_PortListView.as_view(), name='patch_port_list'),
  path('patch_port/add/', Patch_PortCreateView.as_view(), name='patch_port_add'),
  path('patch_port/edit/<int:pk>/', Patch_PortUpadateView.as_view(), name='patch_port_edit'),
  path('patch_port/delete/<int:pk>/', Patch_PortDeleteView.as_view(), name='patch_port_delete'),
  # Wall Ports
  path('wall_port/list/', WallPortListView.as_view(), name='wall_port_list'),
  path('wall_port/add/', WallPortCreateView.as_view(), name='wall_port_add'),
  path('wall_port/edit/<int:pk>/', WallPortUpdateView.as_view(), name='wall_port_edit'),
  path('wall_port/delete/<int:pk>/', WallPortDeleteView.as_view(), name='wall_port_delete'),

  # DEVICES
  # Brands
  path('brand/list/', BrandListView.as_view(), name='brand_list'),
  path('brand/add/', BrandCreateView.as_view(), name='brand_add'),
  path('brand/edit/<int:pk>/', BrandUpadateView.as_view(), name='brand_edit'),
  path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete'),
  # Dev_Type
  path('dev_type/list/', Dev_TypeListView.as_view(), name='dev_type_list'),
  path('dev_type/add/', Dev_TypeCreateView.as_view(), name='dev_type_add'),
  path('dev_type/edit/<int:pk>/', Dev_TypeUpadateView.as_view(), name='dev_type_edit'),
  path('dev_type/delete/<int:pk>/', Dev_TypeDeleteView.as_view(), name='dev_type_delete'),
  # Dev_Status
  path('dev_status/list/', DevStatusListView.as_view(), name='dev_status_list'),
  path('dev_status/add/', Dev_StatusCreateView.as_view(), name='dev_status_add'),
  path('dev_status/edit/<int:pk>/', Dev_StatusUpadateView.as_view(), name='dev_status_edit'),
  path('dev_status/delete/<int:pk>/', Dev_StatusDeleteView.as_view(), name='dev_status_delete'),
  # Models
  path('dev_model/list/', Dev_ModelsListView.as_view(), name='dev_model_list'),
  path('dev_model/add/', Dev_ModelsCreateView.as_view(), name='dev_model_add'),
  path('dev_model/edit/<int:pk>/', Dev_ModelsUpadateView.as_view(), name='dev_model_edit'),
  path('dev_model/delete/<int:pk>/', Dev_ModelsDeleteView.as_view(), name='dev_model_delete'),
  # Devices
  path('device/list/', DeviceListView.as_view(), name='device_list'),
  #Tryng to start Select2
  # path('device/add/', DeviceCreateView.as_view(), name='device_add'),
  path('device/add/', DeviceCreateView.as_view(), name='device_add'),
  path('device/edit/<int:pk>/', DeviceUpdateView.as_view(), name='device_edit'),
  path('device/delete/<int:pk>/', DeviceDeleteView.as_view(), name='device_delete'),

  # DINAMIC TABLES
  # Employee_Status
  path('employee_status/list/', EmployeeStatusListView.as_view(), name='employee_status_list'),
  path('employee_status/add/', EmployeeStatusCreateView.as_view(), name='employee_status_add'),
  path('employee_status/edit/<int:pk>/', EmnployeeStatusUpdateView.as_view(), name='employee_status_edit'),
  path('employee_status/delete/<int:pk>/', EmployeeStatusDeleteView.as_view(), name='employee_status_delete'),
  # Employee
  path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
  path('employee/add/', EmployeeCreateView.as_view(), name='employee_add'),
  path('employee/edit/<int:pk>/', EmployeeUpadateView.as_view(), name='employee_edit'),
  path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
  # Techs
  path('techs/list/', TechsListView.as_view(), name='techs_list'),
  path('techs/add/', TechsCreateView.as_view(), name='techs_add'),
  path('techs/edit/<int:pk>/', TechsUpadateView.as_view(), name='techs_edit'),
  path('techs/delete/<int:pk>/', TechsDeleteView.as_view(), name='techs_delete'),

  # DEVICES & SUPLYES
  # Suply Type
  path('suply_type/list/', SuplyTypeListView.as_view(), name='suply_type_list'),
  path('suply_type/add/', SuplyTypeCreateView.as_view(), name='suply_type_add'),
  path('suply_type/edit/<int:pk>/', SuplyTypeUpadateView.as_view(), name='suply_type_edit'),
  path('suply_type/delete/<int:pk>/', SuplyTypeDeleteView.as_view(), name='suply_type_delete'),
  # Suply
  path('suply/list/', SuplyListView.as_view(), name='suply_list'),
  path('suply/add/', SuplyCreateView.as_view(), name='suply_add'),
  path('suply/edit/<int:pk>/', SuplyUpadateView.as_view(), name='suply_edit'),
  path('suply/delete/<int:pk>/', SuplyDeleteView.as_view(), name='suply_delete'),
]
