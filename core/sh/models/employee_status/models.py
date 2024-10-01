from django.db import models
from django.forms import model_to_dict

class Employee_Status(models.Model):
  status = models.CharField(max_length=35, verbose_name='Estado Empleado')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.status

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Estado Empleado'
    verbose_name_plural = 'Estados de Empleados'
    db_table = 'estados_empleados'
    ordering = ['id']