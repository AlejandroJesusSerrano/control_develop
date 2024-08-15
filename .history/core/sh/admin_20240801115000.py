from django.contrib import admin
from core.sh.models import *

# Equipos
class BrandAdmin(admin.ModelAdmin):

  list_display = ('brand', 'date_creation', 'date_updated')
  list_instances = True
  search_fields = ['brand']

admin.site.register(Brand, BrandAdmin)

admin.site.register(Dev_Type)
admin.site.register(Dev_Status)
admin.site.register(Dev_Model)
admin.site.register(Connection_Type)

class DeviceAdmin(admin.ModelAdmin):

  list_display = ('get_type', 'get_brand', 'dev_model', 'connection', 'ip', 'dev_status', 'get_employee', 'office', 'get_wallPort', 'get_switchPort')
  list_instances = True
  search_fields = ['dev_model__dev_type__dev_type','dev_model__dev_model','dev_model__brand__brand','ip', 'serial_n', 'net_name', 'office', 'get_wallPort__wall_port', 'get_switchPort__port_id']
  list_filter = ['dev_model__dev_type__dev_type','dev_model__dev_model','dev_model__brand__brand','ip', 'serial_n', 'net_name', 'office', 'get_wallPort__wall_port', 'get_switchPort__port_id']
  ordering = ['dev_model__dev_model','dev_model__brand__brand', 'serial_n', 'net_name']

  def get_type(self,obj):
    return obj.dev_model.dev_type.dev_type
  get_type.short_description = 'Tipo'

  def get_brand(self, obj):
    return obj.dev_model.brand.brand
  get_brand.short_description = 'Marca'

  def get_employee(self, obj):
    return " / ".join([f"{empl.employee_last_name}, {empl.employee_name}" for empl in obj.employee.all()])
  get_employee.short_description = 'Empleado'

  def get_wallPort(self, obj):
    return obj.wall_port.wall_port if obj.wall_port else 'No se conecta a boca de Pared'
  get_wallPort.short_description = 'Boca Pared'

  def get_switchPort(self, obj):
    return obj.switch_port.port_id if obj.switch_port else 'No hay switch intermedio'
  get_wallPort.short_description = 'Boca Switch'

admin.site.register(Device, DeviceAdmin)

# Switchs & Ports
admin.site.register(Rack)
admin.site.register(Patchera)
admin.site.register(Patch_Port)
admin.site.register(Switch)
admin.site.register(Switch_Port)
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

