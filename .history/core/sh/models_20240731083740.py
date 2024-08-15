from django.db import models
from datetime import datetime

from django.forms import model_to_dict
# Create your models here.
class Brand(models.Model):
  brand = models.CharField(max_length=50, verbose_name = 'Marca')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Regilstro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.brand

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Marca'
    verbose_name_plural = 'Marcas'
    db_table = 'marca'
    ordering = ['brand']

class Dev_Type(models.Model):
  dev_type = models.CharField(max_length = 50, verbose_name = 'Tipo de Dispositivo')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Regilstro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.dev_type

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tipo de Dispositivo'
    verbose_name_plural = 'Tipos de Dispositivo'
    db_table = 'tipo_de_dispositivo'
    ordering = ['id']

class Dev_Status(models.Model):
  dev_status = models.CharField(max_length = 33, verbose_name = 'Estado del Dispositivo')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Regilstro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.dev_status

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Estado del Dispositivo'
    verbose_name_plural = 'Estados de los Dispositivos'
    db_table = 'estado_del_dispositivo'
    ordering = ['id']

class Dev_Model(models.Model):
  dev_type = models.ForeignKey(Dev_Type, related_name = 'models_dev_type', verbose_name = 'Tipo de Dispositivo', on_delete = models.CASCADE)
  brand = models.ForeignKey(Brand, related_name = 'models_brand', verbose_name = 'Marca', on_delete = models.CASCADE)
  dev_model = models.CharField(max_length = 50, verbose_name = 'Modelo')
  image = models.ImageField(upload_to='img_models/%Y/%m/%d', null = True, blank = True, verbose_name = 'Imagen')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.dev_model

  def toJSON(self):
    item = model_to_dict(self)
    item['dev_type'] = self.dev_type.dev_type
    item['brand'] = self.brand.brand
    item['image'] = self.image.url if self.image else '/media/no_file.svg'
    return item

  class Meta:
    verbose_name = 'Modelo'
    verbose_name_plural = 'Modelos'
    db_table = 'modelo'
    ordering = ['id']

class Techs(models.Model):
  name = models.CharField(max_length = 75, verbose_name = 'Nombre')
  last_name = models.CharField(max_length = 75, verbose_name = 'Apellido')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.last_name}, {self.name}'

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tecnico'
    verbose_name_plural = 'Tecnicos'
    db_table = 'tecnico'
    ordering = ['id']

class Province(models.Model):
  number_id = models.CharField(max_length = 2, verbose_name = 'Numero de Distrito', unique=True)
  province = models.CharField(max_length = 50, verbose_name = 'Nombre de Provincia', unique=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.province

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Provincia'
    verbose_name_plural = 'Provincias'
    db_table = 'provincias'
    ordering = ['id']

class Location(models.Model):
  province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name = 'Provincia')
  location = models.CharField(max_length = 75, verbose_name = 'Localidad')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.location

  def toJSON(self):
    item = model_to_dict(self)
    item['province'] = self.province.province
    return item

  class Meta:
    verbose_name = 'Localidad'
    verbose_name_plural = 'Localidades'
    db_table = 'localidades'
    ordering = ['id']

class Edifice(models.Model):
  location = models.ForeignKey(Location, on_delete = models.CASCADE, verbose_name = 'Localidad')
  edifice = models.CharField(max_length = 50, verbose_name = 'Edificio')
  address = models.TextField(verbose_name = 'Domicilio')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')
  def __str__(self):
    return  f'{self.edifice} - {self.address} - {self.location.location} / {self.location.province.province}'

  def toJSON(self):
    item = model_to_dict(self)
    item['province'] = self.location.province.province
    item['location'] = self.location.location
    return item

  class Meta:
    verbose_name = 'Edificio'
    verbose_name_plural = 'Edificios'
    db_table = 'edificios'
    ordering = ['id']

class Dependency(models.Model):
  edifice = models.ForeignKey(Edifice, related_name='dependency_edifice', verbose_name='Edificio', on_delete = models.CASCADE)
  description = models.CharField(max_length = 75, verbose_name = 'Dependencia')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.description

  def toJSON(self):
    item = model_to_dict(self)
    item['dependency'] = self.description
    return item

  class Meta:
    verbose_name = 'Dependencia'
    verbose_name_plural = 'Dependencias'
    db_table = 'dependencia'
    ordering = ['id']

class Office(models.Model):
  dependency = models.ForeignKey(Dependency, related_name = 'offices_dependencies', verbose_name = 'Dependencia', on_delete=models.CASCADE)
  office = models.CharField(max_length = 50, verbose_name = 'Oficina')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.office

  def toJSON(self):
    item = model_to_dict(self)
    item['location'] = self.dependency.edifice.location.location
    item['edifice'] = self.dependency.edifice.edifice
    item['dependency'] = self.dependency.description
    item['office'] = self.office
    return item


  class Meta:
    verbose_name = 'Officina'
    verbose_name_plural = 'Oficinas'
    db_table = 'oficina'
    ordering = ['id']

class Employee_Status(models.Model):
  status = models.CharField(max_length=35, verbose_name='Estado')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.status

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Estado'
    verbose_name_plural = 'Estados'
    db_table = 'estado'
    ordering = ['id']

class Employee(models.Model):

  employee_name = models.CharField(max_length = 50, verbose_name = 'Nombre del Empleado')
  employee_last_name = models.CharField(max_length = 50, verbose_name = 'Apellido')
  cuil = models.CharField(max_length = 11, verbose_name = 'cuil')
  status = models.ForeignKey(Employee_Status, related_name='emmployee_employee_status', verbose_name='Estado', on_delete=models.CASCADE)
  user_pc = models.CharField(max_length = 11, verbose_name = 'Nombre de Usuario')
  office = models.ForeignKey(Office, related_name = 'employee_office', verbose_name = 'Oficina',  on_delete = models.CASCADE,)
  avatar = models.ImageField(upload_to='img_avatars/%Y/%m/%d', null = True, blank = True, verbose_name = 'Avatar')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.employee_last_name}, {self.employee_name} - {self.cuil} - {self.office.office} - {self.status}'

  def employee_full_name(self):
    return f'{self.employee_last_name}, {self.employee_name}'

  def toJSON(self):
    item = model_to_dict(self)
    item['office'] = self.office.office
    item['status'] = self.status.status
    item['avatar'] = self.avatar.url if self.avatar else '/media/no_file.svg'
    return item

  class Meta:
    verbose_name = 'Empleado'
    verbose_name_plural = 'Empleados'
    db_table = 'empleados'
    ordering = ['id']

class Connection_Type(models.Model):
  connection_type = models.CharField(max_length = 30, verbose_name='Tipo de Conexión')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.connection_type

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tipo de Conexión'
    verbose_name_plural = 'Tipos de Conexiónes'
    db_table = 'tipo_de_conexion'
    ordering = ['id']

class Rack(models.Model):
  rack = models.CharField(max_length = 6, verbose_name = 'Rack')
  details = models.TextField(verbose_name = 'Detalle')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.rack}'

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Rack '
    verbose_name_plural = 'Racks'
    db_table = 'rack'
    ordering = ['id']

class Patchera(models.Model):
  rack = models.ForeignKey(Rack, related_name = 'patchera_rack', verbose_name = 'Rack', on_delete = models.CASCADE)
  patch = models.CharField(max_length = 2, verbose_name='Patchera')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.patch

  def toJSON(self):
    item = model_to_dict(self)
    item['rack'] = self.rack.rack
    return item

  class Meta:
    verbose_name = 'Patchera'
    verbose_name_plural = 'Patcheras'
    db_table = 'patchs'
    ordering = ['id']

class Patch_Port(models.Model):
  patch = models.ForeignKey(Patchera, related_name = 'patchera_port', verbose_name = 'Patchera', on_delete = models.CASCADE)
  port = models.CharField(max_length = 2, verbose_name='Puerto')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'PUERTO: {self.port} PATCHERA: {self.patch} DEL RACK: {self.patch.rack}'

  def toJSON(self):
    item = model_to_dict(self)
    item['rack'] = self.patch.rack.rack
    item['patch'] = self.patch.patch
    return item

  class Meta:
    verbose_name = 'Puerto Patchera'
    verbose_name_plural = 'Puertos Patcheras'
    db_table = 'patchs_ports'
    ordering = ['id']

class Switch(models.Model):
  brand = models.ForeignKey(Brand, related_name = 'switch_brand', verbose_name = 'Marca', on_delete = models.CASCADE)
  serial_n = models.CharField(max_length = 20, verbose_name='N° de Serie', null = True, blank = True)
  ports_q = models.CharField(max_length = 2, verbose_name = 'Cantidad de Puertos')
  rack = models.ForeignKey(Rack, related_name = 'switch_rack', verbose_name = 'Rack', on_delete = models.CASCADE, null = True, blank = True)
  switch_rack_pos = models.CharField(max_length = 2, verbose_name = 'Posición en el Rack', blank=True, null=True)
  office = models.ForeignKey(Office, related_name = 'switch_office', verbose_name = 'Oficina', on_delete = models.CASCADE, blank=True, null=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.brand.brand} - PUERTOS: {self.ports_q} N°/S: {self.serial_n} -> DEL RACK: {self.rack} EN LA POSICION: {self.switch_rack_pos}' if self.rack else f'{self.brand.brand} - PUERTOS: {self.ports_q} N°/S: {self.serial_n} -> OFICINA: {self.office}'

  def toJSON(self):
    item = model_to_dict(self)
    item['brand'] = self.brand.brand
    item['rack'] = self.rack.rack
    return item

  class Meta:
    verbose_name = 'Switch'
    verbose_name_plural = 'Switches'
    db_table = 'switchs'
    ordering = ['id']

class Switch_Port(models.Model):
  switch = models.ForeignKey(Switch, related_name = 'ports_switch', verbose_name = 'Switch', on_delete = models.CASCADE)
  port_id = models.CharField(max_length = 3, verbose_name = 'Puerto del Switch')
  patch_port_out = models.OneToOneField(Patch_Port, related_name = 'port_patch_port_out', verbose_name= 'Puerto Patchera Salida', null = True, blank = True, on_delete = models.CASCADE)
  patch_port_in = models.OneToOneField(Patch_Port, related_name = 'port_patch_port_in', verbose_name = 'Puerto Patchera Entrada', null = True, blank = True, on_delete = models.CASCADE)
  switch_in = models.ForeignKey(Switch, related_name = 'ports_switch_in', verbose_name = 'Switch de Ingreso', null=True, blank=True, on_delete = models.CASCADE)
  switch_out = models.ForeignKey(Switch, related_name = 'ports_switch_out', verbose_name = 'Switch de Salida', null = True, blank = True, on_delete = models.CASCADE)
  obs = models.TextField(verbose_name = 'observaciones', null = True, blank = True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.switch.rack}  - PUERTO: {self.port_id} - EXTENSION INGRESO: {self.switch_in} - SALIDA A EXTENSION: {self.switch_out}'

  def toJSON(self):
    item = model_to_dict(self)
    item['rack'] = self.switch.rack.rack if self.switch and self.switch.rack else 'NO RACK'
    item['switch'] = str(self.switch.brand) +'-> '+str(self.switch.ports_q)+'-> Rack Pos: '+str(self.switch.switch_rack_pos)
    item['patch_out'] = 'SI' if self.patch_port_out else 'NO'
    item['patch_port_out'] = str(self.patch_port_out.patch.rack.rack) +' patchera: '+str(self.patch_port_out.patch.patch)+'puerto: '+str(self.patch_port_out.port) if self.patch_port_out and self.patch_port_out.patch else 'NO PATCH'
    item['patch_in'] = 'SI' if self.patch_port_in else 'NO'
    item['patch_port_in'] = str(self.patch_port_in.patch.rack.rack) +' patchera: '+str(self.patch_port_in.patch.patch)+'puerto: '+str(self.patch_port_in.port) if self.patch_port_in and self.patch_port_in.patch else 'NO PATCH'
    item['switchIn'] = 'SI' if self.switch_in else 'NO'
    item['switch_in'] = str(self.switch_in.rack.rack) +' switch: '+str(self.switch_in.switch_rack_pos) if self.switch_in and self.switch_in.rack else 'NO SWITCH'
    item['switchOut'] = 'SI' if self.switch_out else 'NO'
    item['switch_out'] = str(self.switch_out.rack.rack) +' switch: '+str(self.switch_out.switch_rack_pos) if self.switch_out and self.switch_out.rack else 'NO SWITCH'
    item['obs'] = str(self.obs) if self.obs else 'NO HAY OBSERVACIONES'
    return item

  class Meta:
    verbose_name = 'Puerto de Switch'
    verbose_name_plural = 'Puertos de Switchs'
    db_table = 'puertos_switchs'
    ordering = ['id']

class Wall_Port(models.Model):
    office = models.ForeignKey(Office, related_name='office_wall_port', verbose_name='Oficina', on_delete=models.CASCADE)
    wall_port = models.CharField(max_length=8, verbose_name='Boca Pared')
    switch_port_in = models.OneToOneField(Switch_Port, related_name='wall_switch_port_in', verbose_name='Puerto del Switch Padre', on_delete=models.CASCADE, null=True, blank=True)
    switch_port_out = models.OneToOneField(Switch_Port, related_name='wall_switch_port_out', verbose_name='Switch Hijo', on_delete=models.CASCADE, null=True, blank=True)
    details = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name='Última Modificación')

    def __str__(self):
        switch_info = f'-> SWITCH: {self.switch_port_out.switch.brand} DE {self.switch_port_out.switch.ports_q} BOCAS EN EL PUERTO {self.switch_port_out.port_id}'  if self.switch_port_out else 'NO SWITCH'
        patch_port_in_info = f"PATCHERA: {self.switch_port_in.patch_port_out.patch} -> PUERTO: {self.switch_port_in.patch_port_out.port}" if self.switch_port_in.patch_port_out else "NO PATCH"
        patch_port_out_info = f"PATCHERA: {self.switch_port_in.patch_port_in.patch} -> PUERTO: {self.switch_port_in.patch_port_in.port}" if self.switch_port_in.patch_port_in else "NO PATCH"
        switch_port_in_info = f"SWITCH/RACK: {self.switch_port_in.switch.switch_rack_pos} -> PUERTO: {self.switch_port_in.port_id} -> RACK: {self.switch_port_in.switch.rack}" if self.switch_port_in else "No SWITCH"
        switch_port_out_info = f"SWITCH: {self.switch_port_in.switch_out.brand} -> DE {self.switch_port_in.switch_out.ports_q} BOCAS"  if self.switch_port_in.switch_out else "NO SWITCH"
        return f'BOCA: {self.wall_port} EN OFICINA {self.office.office} {switch_info} -> {patch_port_out_info} -> {switch_port_out_info} -> {patch_port_in_info} -> {switch_port_in_info}'

    def toJSON(self):
        item = model_to_dict(self)
        item['office'] = self.office.office
        item['wall_port'] = self.wall_port
        item['switch_port_in'] = 'RACK: '+str(self.switch_port_in.switch.rack)+'-> SWITCH: '+str(self.switch_port_in.switch.switch_rack_pos)+'-> PUERTO: '+str(self.switch_port_in.port_id) if self.switch_port_in else 'NO SWITCH'
        item['switch_port_out'] = 'RACK: '+str(self.switch_port_out.switch.rack)+'-> SWITCH: '+str(self.switch_port_out.switch.switch_rack_pos)if self.switch_port_out else 'NO SWITCH'
        item['details'] = self.details if self.details else 'SIN DETALLES'
        return item

    class Meta:
        verbose_name = 'Boca Pared'
        verbose_name_plural = 'Bocas Pared'
        db_table = 'wall_port'
        ordering = ['id']

class Device(models.Model):
  dev_model = models.ForeignKey(Dev_Model, related_name='device_model', verbose_name='Modelo de Dispositivo', on_delete=models.CASCADE)
  dev_status = models.ForeignKey(Dev_Status, related_name='device_status', verbose_name='Estado del Dispositivo', on_delete=models.CASCADE)
  connection = models.ForeignKey(Connection_Type, related_name='device_connection', verbose_name='Conexion del Dispositivo', on_delete=models.CASCADE)
  ip = models.CharField(max_length = 15, verbose_name='IP', blank=True, null=True)
  serial_n = models.CharField(max_length = 20, verbose_name='S/N°')
  net_name = models.CharField(max_length = 11, verbose_name='ID en la Red', blank=True, null=True)
  office = models.ForeignKey(Office, related_name = 'device_office', verbose_name = 'Oficina', on_delete = models.CASCADE)
  wall_port = models.ForeignKey(Wall_Port, related_name = 'device_wall_port', verbose_name='Boca de la pared', on_delete=models.CASCADE, blank=True, null=True)
  switch_port = models.ForeignKey(Switch_Port, related_name='device_switch_port', verbose_name='Puerto de Switch', on_delete=models.CASCADE, blank=True, null=True)
  employee = models.ManyToManyField(Employee, related_name='device_employee', verbose_name='Empleado')

  def __str__(self):
    employees = self.employee.all()
    empl_str =', '.join([f"{empl.employee_last_name}, {empl.employee_name}, Oficina: {empl.office.office}" for empl in employees])
    return f'{self.dev_model.dev_type} Marca: {self.dev_model.brand}, Modelo: {self.dev_model.dev_model}, S/N°: {self.serial_n}, Empleado: {empl_str}'

  def toJSON(self):
      item = model_to_dict(self)
      item['type'] = self.dev_model.dev_type.dev_type
      item['brand'] = self.dev_model.brand.brand
      item['model'] = self.dev_model.dev_model
      item['w_port'] = self.wall_port.wall_port if self.wall_port else 'No se conecta a puerto de pared'
      item['s_port'] = self.switch_port.switch.ports_q if self.switch_port else 'No se conecta a Switch intermedio'
      item['office'] = self.office.office
      item['employees'] = [
        {
          'name': e.employee_name,
          'last_name': e.employee_last_name,
          'office': e.office.office if e.office else 'No asignada'
        }
        for e in self.employee.all()]
      return item

  class Meta:
    verbose_name = 'Dispositivo'
    verbose_name_plural = 'Dispositivos'
    db_table = 'dispositivos'
    ordering = ['id']

class Suply_Type(models.Model):
  suply_type = models.CharField(max_length = 20, verbose_name = 'Tipo de Insumo')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.suply_type
  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tipo de Insumo'
    verbose_name_plural = 'Tipos de Insumos'
    db_table = 'tipos_insumos'
    ordering = ['id']

class Suply(models.Model):
  suply_type = models.ForeignKey(Suply_Type, related_name = 'suply_suply_type', verbose_name = 'Tipo de Insumo', on_delete = models.CASCADE)
  dev_model = models.ForeignKey(Dev_Model, related_name = 'suply_dev_model', verbose_name = 'Modelo de Dispositivo', on_delete = models.CASCADE)
  serial_suply = models.CharField(max_length = 25, verbose_name = 'Número de Serie')
  date_in = models.DateField(auto_now = False, auto_now_add= False, verbose_name= 'Fecha de Ingreso')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.suply_type} - {self.dev_model.brand} - {self.dev_model.dev_model}'

  def toJSON(self):
    item = model_to_dict(self)
    item['dev_model'] = self.dev_model.dev_model
    item['brand'] = self.dev_model.brand.brand
    item['date_in'] = self.date_in.strftime('%d/%m/%y')
    return item

  class Meta:
    verbose_name = 'Insumo'
    verbose_name_plural = 'Insumos'
    db_table = 'insumos'
    ordering = ['id']

class Move_Type(models.Model):
  move = models.CharField(max_length = 20, verbose_name = 'Movimiento')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.move

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tipo de Movimiento'
    verbose_name_plural = 'Tipos Movimientos'
    db_table = 'tipo_movimiento'
    ordering = ['id']

class Movements(models.Model):
  device = models.ForeignKey(Device, related_name = 'movement_device', verbose_name = 'Dispositivo', on_delete = models.CASCADE)
  move = models.ForeignKey(Move_Type, related_name = 'movement_move_type', verbose_name = 'Movimiento', on_delete = models.CASCADE)
  techs = models.ForeignKey(Techs, related_name = 'movement_techs', verbose_name = 'Técnico', on_delete = models.CASCADE)
  date = models.DateField(auto_created = False, auto_now = False, auto_now_add = False, verbose_name='Fecha de realización')
  suply = models.ForeignKey(Suply, related_name = 'movement_suply', verbose_name = 'Insumo', on_delete = models.CASCADE, null = True, blank = True)
  detail = models.TextField(verbose_name = 'Detalle', null = True, blank = True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')
  def __str__(self):
    return f'{self.move.move} - {self.date} - {self.techs.last_name}, {self.techs.name}'

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Movimiento'
    verbose_name_plural = 'Movimientos'
    db_table = 'movimientos'
    ordering = ['id']