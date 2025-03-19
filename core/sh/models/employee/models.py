from django.db import models 
from django.forms import model_to_dict

from ..employee_status.models import Employee_Status
from ..office.models import Office

class Employee(models.Model):
  employee_name = models.CharField(max_length=50, verbose_name='Nombre del Empleado')
  employee_last_name = models.CharField(max_length=50, verbose_name='Apellido')
  cuil = models.CharField(max_length=11, verbose_name='cuil', unique=True)
  status = models.ForeignKey(Employee_Status, related_name='employee_employee_status', verbose_name='Estado', on_delete=models.CASCADE)
  user_pc = models.CharField(max_length=11, verbose_name='Nombre de Usuario')
  office = models.ForeignKey(Office, related_name='employee_office', verbose_name='Oficina', on_delete=models.CASCADE)
  avatar = models.ImageField(upload_to='img_avatars/%Y/%m/%d', null=True, blank=True, verbose_name='Avatar')
  notes = models.TextField(null=True, blank=True, verbose_name='Observaciones')
  date_creation = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add=True, verbose_name='Última Modificación')

  def save(self, *args, **kwargs):
    self.employee_name = self.employee_name.upper()
    self.employee_last_name = self.employee_last_name.upper()
    self.user_pc = self.user_pc.upper()
    super(Employee, self).save(*args, **kwargs)

  def __str__(self):
    return f'{self.employee_last_name}, {self.employee_name} - CUIL Nro: {self.cuil} / Usuario: {self.user_pc} - {self.office.office} - {self.status}'

  def employee_full_name(self):
    return f'{self.employee_last_name}, {self.employee_name}'

  def toJSON(self):
    item = model_to_dict(self)
    item['id'] = self.id
    item['employee_full_name'] = (f"{self.employee_last_name}, {self.employee_name}")
    item['cuil'] = self.cuil
    item['status'] = self.status.status
    item['user_pc'] = self.user_pc
    item['office'] = (f"{self.office.office} / Localidad: {self.office.loc.edifice.location.location} / Provincia: {self.office.loc.edifice.location.province.province}")
    item['dependency'] = self.office.dependency.dependency
    item['avatar'] = self.avatar.url if self.avatar else '/media/no_file.svg'
    return item

  class Meta:
    verbose_name = 'Empleado'
    verbose_name_plural = 'Empleados'
    db_table = 'empleados'
    ordering = ['id']
    constraints = [
      models.UniqueConstraint(fields=['cuil', 'office'], name = 'unique_cuil_office')
    ]