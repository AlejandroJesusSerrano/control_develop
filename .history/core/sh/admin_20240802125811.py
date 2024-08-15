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

class SwitchAdmin(admin.ModelAdmin):

  list_display = ('rack', 'brand','serial_n', 'switch_rack_pos', 'ports_q', 'office')
  list_instances = True
  search_fields = ['brand__brand', 'serial_n', 'ports_q', 'rack__rack', 'switch_rack_pos', 'office__office']
  list_filter = ['brand__brand', 'ports_q', 'rack__rack', 'office__office']
  ordering = ['brand__brand', 'serial_n', 'ports_q', 'rack__rack', 'switch_rack_pos', 'office__office']

admin.site.register(Switch, SwitchAdmin)

class SwitchPortAdmin(admin.ModelAdmin):

  list_display = ('get_switch_rack','get_switch_brand', 'get_switch_ports', 'get_switch_rack_pos', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out', 'obs')
  list_instances = True
  search_fields = ['switch__rack__rack', 'switch__switch_rack_pos', 'switch__brand__brand', 'switch__ports_q', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out', 'obs']
  list_filter = ['switch__rack__rack', 'switch__switch_rack_pos', 'switch__brand__brand', 'switch__ports_q', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out', 'obs']
  ordering = ['switch__rack__rack', 'switch__switch_rack_pos', 'switch__brand__brand', 'switch__ports_q', 'port_id','patch_port_out', 'patch_port_in', 'switch_in', 'switch_out', 'obs']

  def get_switch_rack(self, obj):
    return obj.switch_rack_rack
  get_switch_rack.short_description = 'Rack'
  get_switch_rack.admin_order_field = 'switch__rack__rack'

  def get_switch_rack_pos(self, obj):
    return obj.switch_switch_rack_pos
  get_switch_rack.short_description = 'Posicion en el Rack'
  get_switch_rack.admin_order_field = 'switch__switch_rack_pos'

  def get_switch_brand(self, obj):
    return obj.switch.brand.brand
  get_switch_brand.short_description = 'Marca Switch'
  get_switch_brand.admin_order_field = 'switch__brand__brand'

  def get_switch_ports(self, obj):
    return obj.switch.ports_q
  get_switch_brand.short_description = 'Cantidad de Puertos'
  get_switch_brand.admin_order_field = 'switch__ports_q'

admin.site.register(Switch_Port, SwitchAdmin)


admin.site.register(Wall_Port)

# Suply
admin.site.register(Suply_Type)
admin.site.register(Suply)

# Movements
admin.site.register(Move_Type)
admin.site.register(Movements)

# Tecnicos
admin.site.register(Techs)

# Dependencias y oficinas
admin.site.register(Province)
admin.site.register(Location)
admin.site.register(Edifice)
admin.site.register(Dependency)
admin.site.register(Office)

# Empleados -usuarios de equipos-
admin.site.register(Employee_Status)
admin.site.register(Employee)

