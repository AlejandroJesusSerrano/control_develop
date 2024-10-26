from django.db import models
from django.forms import model_to_dict

class Techs(models.Model):
  name = models.CharField(max_length = 75, verbose_name = 'Nombre')
  last_name = models.CharField(max_length = 75, verbose_name = 'Apellido')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.name = self.name.upper()
    self.last_name = self.last_name.upper()
    super(Techs, self).save(*args, **kwargs)

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
    constraints = [
      models.UniqueConstraint(fields=['name', 'last_name'], name='unique_tech_name')
    ]