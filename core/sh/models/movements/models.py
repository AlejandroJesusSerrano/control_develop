from django.db import models
from django.forms import model_to_dict

from ..switch.models import Switch

from ..device.models import Device
from ..move_type.models import Move_Type
from ..suply.models import Suply
from ..tehcs.models import Techs

class Movements(models.Model):
  device = models.ForeignKey(Device, related_name = 'movement_device', verbose_name = 'Dispositivo', on_delete = models.CASCADE)
  switch = models.ForeignKey(Switch, related_name = 'movement_switch', verbose_name = 'Switch', on_delete = models.CASCADE, null=True, blank=True)
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
    item['device'] = f"{self.device.dev_model.dev_type.dev_type} - {self.device.dev_model.brand.brand} {self.device.dev_model.dev_model} S/N°: {self.device.serial_n}"
    item['switch'] = f"SWITCH {self.switch.model.brand} - {self.switch.model.dev_model} / {self.switch.ports_q}"
    item['move'] = self.move.move
    item['techs'] = f"{self.techs.last_name}, {self.techs.name}"
    item['date'] = self.date
    item['suply'] = self.suply.suply_type if self.suply else 'NO SE REALIZO CAMBIO DE INSUMO'
    return item

  class Meta:
    verbose_name = 'Movimiento'
    verbose_name_plural = 'Movimientos'
    db_table = 'movimientos'
    ordering = ['id']