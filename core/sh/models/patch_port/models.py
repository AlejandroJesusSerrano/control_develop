from django.db import models
from django.forms import model_to_dict

from ..patchera.models import Patchera

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