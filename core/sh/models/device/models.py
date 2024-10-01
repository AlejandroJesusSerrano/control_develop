from django.db import models
from django.forms import model_to_dict

from ..connection_type.models import Connection_Type
from ..dev_status.models import Dev_Status
from ..dev_model.models import Dev_Model
from ..employee.models import Employee
from ..office.models import Office
from ..switch_port.models import Switch_Port
from ..wall_port.models import Wall_Port

class Device(models.Model):
  dev_model = models.ForeignKey(Dev_Model, related_name='device_model', verbose_name='Modelo de Dispositivo', on_delete=models.CASCADE)
  dev_status = models.ForeignKey(Dev_Status, related_name='device_status', verbose_name='Estado del Dispositivo', on_delete=models.CASCADE)
  connection = models.ForeignKey(Connection_Type, related_name='device_connection', verbose_name='Conexion del Dispositivo', on_delete=models.CASCADE, blank=True, null=True)
  ip = models.CharField(max_length=15, verbose_name='IP', blank=True, null=True, unique=True)
  serial_n = models.CharField(max_length=20, verbose_name='S/N°', unique=True)
  net_name = models.CharField(max_length=11, verbose_name='ID en la Red', blank=True, null=True, unique=True)
  office = models.ForeignKey(Office, related_name='device_office', verbose_name='Oficina', on_delete=models.CASCADE)
  wall_port = models.OneToOneField(Wall_Port, related_name='device_wall_port', verbose_name='Boca de la pared', on_delete=models.CASCADE, blank=True, null=True)
  switch_port = models.OneToOneField(Switch_Port, related_name='device_switch_port', verbose_name='Puerto de Switch', on_delete=models.CASCADE, blank=True, null=True)
  employee = models.ManyToManyField(Employee, related_name='device_employee', verbose_name='Empleado', blank=True)

  def __str__(self):
    employees = self.employee.all()
    empl_str = ', '.join([f"{empl.employee_last_name}, {empl.employee_name}, Oficina: {empl.office.office}" for empl in employees])
    return f'{self.dev_model.dev_type} Marca: {self.dev_model.brand}, Modelo: {self.dev_model.dev_model}, S/N°: {self.serial_n}, Empleado: {empl_str}'

  def toJSON(self):
    item = model_to_dict(self)
    item['type'] = self.dev_model.dev_type.dev_type
    item['brand'] = self.dev_model.brand.brand
    item['model'] = self.dev_model.dev_model
    item['w_port'] = self.wall_port.wall_port if self.wall_port else 'No se conecta a puerto de pared'
    item['s_port'] = self.switch_port.switch.ports_q if self.switch_port else 'No se conecta a Switch intermedio'
    item['office'] = self.office.office
    employees = self.employee.all()
    employee_data = [
        {'employee_name': empl.employee_name, 'employee_last_name': empl.employee_last_name}
        for empl in employees
    ]
    item['employee'] = employee_data
    return item

  class Meta:
    verbose_name = 'Dispositivo'
    verbose_name_plural = 'Dispositivos'
    db_table = 'dispositivos'
    ordering = ['id']