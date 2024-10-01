from django.db import models
from django.forms import model_to_dict

from ..dev_model.models import Dev_Model
from ..suply_type.models import Suply_Type

class Suply(models.Model):
  suply_type = models.ForeignKey(Suply_Type, related_name = 'suply_suply_type', verbose_name = 'Tipo de Insumo', on_delete = models.CASCADE)
  dev_model = models.ForeignKey(Dev_Model, related_name = 'suply_dev_model', verbose_name = 'Modelo de Dispositivo', on_delete = models.CASCADE)
  serial_suply = models.CharField(max_length = 25, verbose_name = 'Número de Serie')
  date_in = models.DateField(auto_now = False, auto_now_add= False, verbose_name= 'Fecha de Ingreso')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.suply_type} - {self.dev_model.brand} - {self.dev_model.dev_model}'

  def toJSON(self):
    item = model_to_dict(self)
    item['dev_model'] = self.dev_model.dev_model
    item['brand'] = self.dev_model.brand.brand
    item['date_in'] = self.date_in.strftime('%d/%m/%y')
    return item

  class Meta:
    verbose_name = 'Insumo'
    verbose_name_plural = 'Insumos'
    db_table = 'insumos'
    ordering = ['id']