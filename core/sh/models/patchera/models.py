from django.db import models
from django.forms import model_to_dict

from ..rack.models import Rack

class Patchera(models.Model):
  rack = models.ForeignKey(Rack, related_name = 'patchera_rack', verbose_name = 'Rack', on_delete = models.CASCADE)
  patchera = models.CharField(max_length = 2, verbose_name='Patchera')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.patchera = self.patchera.upper()
    super(Patchera, self).save(*args, **kwargs)

  def __str__(self):
    return self.patchera

  def toJSON(self):
    item = model_to_dict(self)
    item['rack'] = self.rack.rack
    item['patchera'] = self.patchera
    return item

  class Meta:
    verbose_name = 'Patchera'
    verbose_name_plural = 'Patcheras'
    db_table = 'patchs'
    ordering = ['id']
    constraints = [
        models.UniqueConstraint(fields=['rack', 'patchera'], name='unique_rack_patchera')
    ]