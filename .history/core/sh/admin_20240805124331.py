from django.contrib import admin
from core.sh.models import *

# Equipos
class BrandAdmin(admin.ModelAdmin):

  list_display = ('brand', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['brand']
  ordering = ['brand']

admin.site.register(Brand, BrandAdmin)

class TypeAdmin(admin.ModelAdmin):

  list_display = ('dev_type', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['dev_type']
  ordering = ['dev_type']

admin.site.register(Dev_Type, TypeAdmin)

class StatusAdmin(admin.ModelAdmin):

  list_display = ('dev_status', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['dev_status']
  ordering = ['dev_status']

admin.site.register(Dev_Status, StatusAdmin)

class DevModelAdmin(admin.ModelAdmin):

  list_display = ('dev_type', 'brand', 'dev_model', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['dev_type__dev_type', 'brand__brand', 'dev_model', 'date_creation', 'date_updated']
  ordering = ['dev_type__dev_type', 'brand__brand', 'dev_model', 'date_creation', 'date_updated']

admin.site.register(Dev_Model, DevModelAdmin)

class ConnectionAdmin(admin.ModelAdmin):

  list_display = ('connection_type', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['connection_type']
  ordering = ['connection_type']

admin.site.register(Connection_Type, ConnectionAdmin)

class DeviceAdmin(admin.ModelAdmin):

  list_display = ('get_type', 'get_brand', 'dev_model', 'connection', 'ip', 'dev_status', 'get_employee', 'office', 'get_wallPort', 'get_switchPort')
  list_instances = True

  search_fields = [
    'dev_model__dev_type__dev_type',
    'dev_model__brand__brand',
    'dev_model__dev_model',
    'ip',
    'serial_n',
    'net_name',
    'employee__employee_last_name',
    'employee__employee_name',
    'office__office',
    'wall_port__wall_port',
    'switch_port__port_id'
    ]

  list_filter = [
    'dev_model__dev_type__dev_type',
    'dev_model__brand__brand',
    'dev_model__dev_model',
    'ip',
    'serial_n',
    'net_name',
    'employee__employee_last_name',
    'office__office',
    'wall_port__wall_port',
    'switch_port__port_id'
    ]

  ordering = [
    'dev_model__dev_type__dev_type',
    'dev_model__brand__brand',
    'dev_model__dev_model','ip',
    'serial_n',
    'net_name',
    'office__office',
    'wall_port__wall_port',
    'switch_port__port_id'
    ]

  def get_type(self,obj):
    return obj.dev_model.dev_type.dev_type
  get_type.short_description = 'Tipo'
  get_type.admin_order_field = 'dev_model__dev_type__dev_type'

  def get_brand(self, obj):
    return obj.dev_model.brand.brand
  get_brand.short_description = 'Marca'
  get_brand.admin_order_field = 'dev_model__brand__brand'

  def get_employee(self, obj):
    employees = " / ".join([f"{empl.employee_last_name}, {empl.employee_name}" for empl in obj.employee.all()])
    return employees
  get_employee.short_description = 'Empleado'

  def get_wallPort(self, obj):
    return obj.wall_port.wall_port if obj.wall_port else 'No se conecta a boca de Pared'
  get_wallPort.short_description = 'Boca Pared'

  def get_switchPort(self, obj):
    return obj.switch_port.port_id if obj.switch_port else 'No hay switch intermedio'
  get_switchPort.short_description = 'Boca Switch'

admin.site.register(Device, DeviceAdmin)

# Switchs & Ports
class RackAdmin(admin.ModelAdmin):

  list_display = ('rack', 'details', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['rack']
  ordering = ['rack']

admin.site.register(Rack, RackAdmin)

class PatchAdmin(admin.ModelAdmin):

  list_display = ('rack', 'patch', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['rack__rack', 'patch']
  ordering = ['rack__rack', 'patch']

admin.site.register(Patchera, PatchAdmin)

class PatchPortAdmin(admin.ModelAdmin):

  list_display = ('get_patchPortRack', 'patch', 'port', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['patch__rack__rack', 'patch__patch', 'port']
  list_filter = ['patch__rack__rack']
  ordering = ['patch__rack__rack', 'patch__patch', 'patch']

  def get_patchPortRack(self, obj):
    return obj.patch.rack.rack
  get_patchPortRack.short_description = 'Rack'
  get_patchPortRack.admin_order_field = 'patch__rack__rack'

admin.site.register(Patch_Port, PatchPortAdmin)

class SwitchAdmin(admin.ModelAdmin):

  list_display = ('rack', 'brand','serial_n', 'switch_rack_pos', 'ports_q', 'office')
  list_instances = True
  search_fields = ['brand__brand', 'serial_n', 'ports_q', 'rack__rack', 'switch_rack_pos', 'office__office']
  list_filter = ['brand__brand', 'ports_q', 'rack__rack', 'office__office']
  ordering = ['brand__brand', 'serial_n', 'ports_q', 'rack__rack', 'switch_rack_pos', 'office__office']

admin.site.register(Switch, SwitchAdmin)

class SwitchPortAdmin(admin.ModelAdmin):

  list_display = ('get_switchRack', 'get_switchRackPos', 'get_switch_brand', 'get_switch_ports', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out', 'obs')
  list_instances = True
  search_fields = ['switch__rack__rack', 'switch__switch_rack_pos', 'switch__brand__brand', 'switch__ports_q', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out']
  list_filter = ['switch__rack__rack', 'switch__switch_rack_pos', 'switch__brand__brand', 'switch__ports_q', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out']
  ordering = ['switch__rack__rack', 'switch__switch_rack_pos', 'switch__brand__brand', 'switch__ports_q', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out']

  def get_switchRack(self, obj):
    return obj.switch.rack.rack
  get_switchRack.short_description = 'Rack'
  get_switchRack.admin_order_field = 'switch__rack__rack'

  def get_switchRackPos(self, obj):
    return obj.switch.switch_rack_pos
  get_switchRackPos.short_description = 'Posicion en el Rack'
  get_switchRackPos.admin_order_field = 'switch__switch_rack_pos'

  def get_switch_brand(self, obj):
    return obj.switch.brand.brand
  get_switch_brand.short_description = 'Marca Switch'
  get_switch_brand.admin_order_field = 'switch__brand__brand'

  def get_switch_ports(self, obj):
    return obj.switch.ports_q
  get_switch_ports.short_description = 'Cantidad de Puertos'
  get_switch_ports.admin_order_field = 'switch__ports_q'

admin.site.register(Switch_Port, SwitchPortAdmin)

class WallPortAdmin(admin.ModelAdmin):

  list_display = ('get_wallOffice', 'get_wallOfficeFloor', 'get_wallOfficeWing', 'wall_port', 'switch_port_in', 'switch_port_out', 'details',)
  list_instances = True
  search_fields = ['office__office', 'office__loc__floor', 'office__loc__wing', 'wall_port', 'switch_port_in', 'switch_port_out']
  list_filter = ['office__office', 'office__loc__floor', 'office__loc__wing', 'wall_port', 'switch_port_in', 'switch_port_out']
  ordering = ['office__office', 'office__loc__floor', 'office__loc__wing', 'wall_port', 'switch_port_in', 'switch_port_out']

  def get_wallOffice(self, obj):
    return obj.office.office
  get_wallOffice.short_description = 'Oficina'
  get_wallOffice.admin_order_field = 'office__office'

  def get_wallOfficeFloor(self, obj):
    return obj.office.loc.floor
  get_wallOfficeFloor.short_description = 'Piso'
  get_wallOfficeFloor.admin_order_field = 'office__loc__floor'

  def get_wallOfficeWing(self, obj):
    return obj.office.loc.wing
  get_wallOfficeWing.short_description = 'Ala'
  get_wallOfficeWing.admin_order_field = 'office__loc__wing'

admin.site.register(Wall_Port, WallPortAdmin)

# Suply
class SuplyTypeAdmin(admin.ModelAdmin):

  list_display = ('id', 'suply_type',)
  list_instances = True
  search_fields = ['suply_type']
  ordering = ['suply_type']

admin.site.register(Suply_Type, SuplyTypeAdmin)

class SuplyAdmin(admin.ModelAdmin):

  list_display = ('suply_type', 'get_devType', 'get_devBrand', 'get_devModel', 'serial_suply', 'date_in')
  list_instances = True
  search_fields = ['suply_type', 'dev_model__dev_type__dev_type', 'dev_model__brand__brand', 'dev_model__dev_model', 'serial_suply', 'date_in']
  list_filter = ['suply_type', 'dev_model__dev_type__dev_type', 'dev_model__brand__brand', 'dev_model__dev_model', 'serial_suply', 'date_in']
  ordering = ['suply_type', 'dev_model__dev_type__dev_type', 'dev_model__brand__brand', 'dev_model__dev_model', 'serial_suply', 'date_in']

  def get_devType(self, obj):
    return obj.dev_model.dev_type.dev_type
  get_devType.short_description = 'Tipo Dispositivo'
  get_devType.admin_order_field = 'dev_model__dev_type__dev_type'

  def get_devBrand(self, obj):
    return obj.dev_model.brand.brand
  get_devBrand.short_description = 'Marca'
  get_devBrand.admin_order_field = 'dev_model__brand__brand'

  def get_devModel(self, obj):
    return obj.dev_model.dev_model
  get_devModel.short_description = 'Modelo'
  get_devModel.admin_order_field = 'dev_model__dev_model'

admin.site.register(Suply, SuplyAdmin)

# Movements
class MoveTypeAdmin(admin.ModelAdmin):

  list_display = ('move', 'details', 'date_creation', 'date_updated',)
  list_instances = True
  search_fields = ['move', 'details']
  list_filter = ['move', 'details',]
  ordering = ['move', 'details',]

admin.site.register(Move_Type, MoveTypeAdmin)

class MovementAdmnin(admin.ModelAdmin):
  list_display = ('get_type', 'date', 'get_brand', 'get_model', 'get_user', 'get_office', 'techs', 'detail')
  list_instances = True

  search_fields = [
    'device__dev_model__dev_type__dev_type',
    'date',
    'device__dev_model__brand__brand',
    'device__dev_model__dev_model',
    'device__employee__employee_last_name',
    'device__employee__employee_name'
    'device__office__office',
    'techs__last_name',
    'detail'
    ]

  list_filter = [
    'device__dev_model__dev_type__dev_type',
    'date',
    'device__dev_model__brand__brand',
    'device__dev_model__dev_model',
    'device__employee__employee_last_name',
    'device__office__office',
    'techs__last_name',
    'detail'
    ]

  ordering = [
    'device__dev_model__dev_type__dev_type',
    'date',
    'device__dev_model__brand__brand',
    'device__dev_model__dev_model',
    'device__office__office',
    'techs__last_name',
    'detail'
    ]

  def get_type(self,obj):
    return obj.device.dev_model.dev_type.dev_type
  get_type.short_description = 'Tipo'
  get_type.admin_order_field = 'device__dev_model__dev_type__dev_type'

  def get_brand(self, obj):
    return obj.device.dev_model.brand.brand
  get_brand.short_description = 'Marca'
  get_brand.admin_order_field = 'device__dev_model__brand__brand'

  def get_model(self, obj):
    return obj.device.dev_model.dev_model
  get_model.short_description = 'Modelo'
  get_model.admin_order_field = 'device__dev_model__dev_model'

  def get_user(self,obj):
    users = " / ".join([f"{usr.employee_last_name}, {usr.employee_name}" for usr in obj.device.employee.all()])
    return users
  get_user.short_description = 'Usuario'

  def get_office(self, obj):
    return obj.device.office.office
  get_office.short_description = 'Oficina'
  get_office.admin_order_field = 'device__office__office'

admin.site.register(Movements, MovementAdmnin)

# Tecnicos
class TechsAdmin(admin.ModelAdmin):

  list_display = ('last_name', 'name', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['last_name', 'name', 'date_creation', 'date_updated']
  list_filter = ['last_name', 'name', 'date_creation', 'date_updated']
  ordering = ['last_name', 'name', 'date_creation', 'date_updated']

admin.site.register(Techs, TechsAdmin)

# Dependencias y oficinas
class ProvinceAdmin(admin.ModelAdmin):

  list_display = ('number_id', 'province', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['number_id', 'province', 'date_creation', 'date_updated']
  list_filter = ['number_id', 'province', 'date_creation', 'date_updated']
  ordering = ['number_id', 'province', 'date_creation', 'date_updated']

admin.site.register(Province, ProvinceAdmin)

class LocationAdmin(admin.ModelAdmin):

  list_display = ('get_province_id', 'get_province', 'location', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['province__number_id', 'province__province', 'location', 'date_creation', 'date_updated']
  list_filter = ['province__number_id', 'province__province', 'location', 'date_creation', 'date_updated']
  ordering = ['province__number_id', 'province__province', 'location', 'date_creation', 'date_updated']

  def get_province_id(self, obj):
    return obj.province.number_id
  get_province_id.short_description = 'ID Prov'
  get_province_id.admin_order_field = 'province__number_id'

  def get_province(self, obj):
    return obj.province.province
  get_province_id.short_description = 'Provincia'
  get_province_id.admin_order_field = 'province__province'

admin.site.register(Location, LocationAdmin)



admin.site.register(Edifice)
admin.site.register(Dependency)
admin.site.register(Office_Loc)
admin.site.register(Office)

# Empleados -usuarios de equipos-
admin.site.register(Employee_Status)
admin.site.register(Employee)

