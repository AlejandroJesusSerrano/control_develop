from django.db import models
from django.forms import model_to_dict

from ..dev_model.models import Dev_Model
from ..dev_type.models import Dev_Type
from ..office.models import Office
from ..rack.models import Rack

class Switch(models.Model):
  model = models.ForeignKey(Dev_Model, related_name = 'switch_model', verbose_name = 'Modelo', on_delete = models.CASCADE)
  serial_n = models.CharField(max_length = 20, verbose_name='N° de Serie', null = True, blank = True)
  ports_q = models.CharField(max_length = 2, verbose_name = 'Cantidad de Puertos')
  rack = models.ForeignKey(Rack, related_name = 'switch_rack', verbose_name = 'Rack', on_delete = models.CASCADE, null = True, blank = True)
  switch_rack_pos = models.CharField(max_length = 2, verbose_name = 'Posición en el Rack', blank=True, null=True)
  office = models.ForeignKey(Office, related_name = 'switch_office', verbose_name = 'Oficina', on_delete = models.CASCADE, blank=True, null=True)
  date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now = True, verbose_name = 'Última Modificación')

  def save(self,*args, **kwargs):
    try:
      switch_dev_type = Dev_Type.objects.get(dev_type = 'SWITCH')
    except Dev_Type.DoesNotExist:
      switch_dev_type = Dev_Type.objects.create(dev_type = 'SWITCH')
    except Dev_Type.MultipleObjectsReturned:
      switch_dev_type = Dev_Type.objects.filter(dev_type = 'SWITCH').first()

    if self.model.dev_type != switch_dev_type:
      self.model.dev_type = switch_dev_type
      self.model.dev_type.save()
      self.model.save()

    if self.serial_n:
      self.serial_n = self.serial_n.upper()
    if self.switch_rack_pos:
      self.switch_rack_pos = self.switch_rack_pos.upper()

    super(Switch, self).save(*args, **kwargs)

  def __str__(self):
    if self.rack:
      return f'{self.model.brand.brand} - PUERTOS: {self.ports_q} N°/S: {self.serial_n} -> DEL RACK: {self.rack} EN LA POSICION: {self.switch_rack_pos}' 
    else:
      return f'{self.model.brand.brand} - PUERTOS: {self.ports_q} N°/S: {self.serial_n} -> OFICINA: {self.office}'

  def toJSON(self):
    item = model_to_dict(self)
    item['brand'] = self.model.brand.brand if self.model and self.model.brand else 'GENÉRICO'
    item['rack'] = self.rack.rack if self.rack else 'NO ESTA EN RACK'
    item['office'] = self.office.office if self.office else 'NO ESTA EN UNA OFICINA'
    item['model'] = self.model.dev_model if self.model else 'GENÉRICO'
    item['switch_rack_pos'] = self.switch_rack_pos if self.rack else 'NO ESTA EN RACK'
    return item

  class Meta:
    verbose_name = 'Switch'
    verbose_name_plural = 'Switches'
    db_table = 'switchs'
    ordering = ['id']
    unique_together = ('model', 'serial_n')
    unique_together = ('rack', 'switch_rack_pos')