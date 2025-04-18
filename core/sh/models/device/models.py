from django.db import models
from django.forms import model_to_dict

from ..connection_type.models import Connection_Type
from ..dev_status.models import Dev_Status
from ..dev_model.models import Dev_Model
from ..employee.models import Employee
from ..office.models import Office

class Device(models.Model):
	dev_model = models.ForeignKey(Dev_Model, related_name='device_model', verbose_name='Modelo de Dispositivo', on_delete=models.CASCADE)
	dev_status = models.ForeignKey(Dev_Status, related_name='device_status', verbose_name='Estado del Dispositivo', on_delete=models.CASCADE)
	connection = models.ForeignKey(Connection_Type, related_name='device_connection', verbose_name='Conexion del Dispositivo', on_delete=models.CASCADE, blank=True, null=True)
	ip = models.CharField(max_length=15, verbose_name='IP', blank=True, null=True, unique=True)
	serial_n = models.CharField(max_length=20, verbose_name='S/N°')
	net_name = models.CharField(max_length=11, verbose_name='ID en la Red', blank=True, null=True, unique=True)
	office = models.ForeignKey(Office, related_name='device_office', verbose_name='Oficina', on_delete=models.CASCADE)
	wall_port_in = models.OneToOneField('sh.Wall_Port', related_name='device_wall_port_in', verbose_name='Boca de la pared', on_delete=models.CASCADE, blank=True, null=True)
	switch_port_in = models.OneToOneField('sh.Switch_Port', related_name='device_switch_port_in', verbose_name='Puerto de Switch', on_delete=models.CASCADE, blank=True, null=True)
	patch_port_in = models.OneToOneField('sh.Patch_Port', related_name='device_patch_port_in', verbose_name='Puerto de patchera de Entrada', on_delete=models.CASCADE, blank=True, null=True)
	employee = models.ManyToManyField(Employee, related_name='device_employee', verbose_name='Empleados', blank=True)
	date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de Registro')
	date_updated = models.DateTimeField(auto_now = True, verbose_name = 'Última Modificación')

	def save(self, *args, **kwargs):
		self.serial_n = self.serial_n.upper()
		if self.net_name:
			self.net_name = self.net_name.upper()
		super (Device, self).save(*args, **kwargs)

	def __str__(self):
		if self.employee.exists():
				emp_str = ", ".join([f"{emp.employee_last_name}, {emp.employee_name}, Oficina: {emp.office.office}" for emp in self.employee.all()])
		else:
				emp_str = "No asignado"
		return f"{self.dev_model.dev_type} Marca: {self.dev_model.brand}, Modelo: {self.dev_model.dev_model}, S/N°: {self.serial_n}, Empleado: {emp_str}"

	def toJSON(self):
		item = model_to_dict(self)
		item['ip']= self.ip if self.ip else 'SIN IP'
		item['type'] = self.dev_model.dev_type.dev_type
		item['brand'] = self.dev_model.brand.brand
		item['model'] = self.dev_model.dev_model
		item['w_port'] = self.wall_port_in.wall_port if self.wall_port_in else 'No se conecta a puerto de pared'
		item['s_port'] = (
			f"Switch: {self.switch_port_in.switch.switch_rack_pos} / Puerto: {self.switch_port_in.port_id}"
			if self.switch_port_in else 'No se conecta directo a Switch'
			)
		item['p_port'] = (
			f'Rack: {self.patch_port_in.patchera.rack} / Patchera: { self.patch_port_in.patchera} / Puerto: {self.patch_port_in.port}'
			if self.patch_port_in else 'No llega directo de patchera'
		)
		item['office'] = self.office.office

		if self.employee.exists():
			item['employee'] = [
				f"{emp.employee_last_name}, {emp.employee_name}"
				for emp in self.employee.all()
			]
		else:
			item['employee'] = 'NO HAY EMPLEADO ASIGNADO'
		return item

	def get_next_connection(self):
		if self.wall_port_in is not None:
			return self.wall_port_in
		elif self.switch_port_in is not None:
			return self.switch_port_in
		elif self.patch_port_in is not None:
			return self.patch_port_in
		return None

	class Meta:
		verbose_name = 'Dispositivo'
		verbose_name_plural = 'Dispositivos'
		db_table = 'dispositivos'
		ordering = ['id']
		constraints = [
			models.UniqueConstraint(fields=['serial_n', 'dev_model'], name='unique_serial_n_dev_model')
		]