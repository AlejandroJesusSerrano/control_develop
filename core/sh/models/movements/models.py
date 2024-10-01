from django.db import models
from django.forms import model_to_dict

from ..device.models import Device
from ..move_type.models import Move_Type
from ..suply.models import Suply
from ..tehcs.models import Techs

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