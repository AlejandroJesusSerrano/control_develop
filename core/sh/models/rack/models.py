from django.db import models
from django.forms import model_to_dict

from ..office.models import Office

class Rack(models.Model):
  office = models.ForeignKey(Office, related_name='rack_office', verbose_name='oficina', on_delete=models.CASCADE)
  rack = models.CharField(max_length = 6, verbose_name = 'Rack', unique=True)
  details = models.TextField(verbose_name = 'Detalle')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self,*args, **kwargs):
    self.rack = self.rack.upper()
    self.details = self.details.upper()
    super(Rack, self).save(*args, **kwargs)

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