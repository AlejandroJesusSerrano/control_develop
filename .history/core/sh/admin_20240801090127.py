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

  list_display = ('dev_model.brand', 'dev_model', 'dev_status')
  list_instances = True
  search_fields = ['dev_model']

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

