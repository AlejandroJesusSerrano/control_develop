from django.db import models
from django.forms import model_to_dict

class Suply_Type(models.Model):
  suply_type = models.CharField(max_length = 23, verbose_name = 'Tipo de Insumo', unique=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.suply_type = self.suply_type.upper()
    super(Suply_Type, self).save(*args, **kwargs)

  def __str__(self):
    return self.suply_type
  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tipo de Insumo'
    verbose_name_plural = 'Tipos de Insumos'
    db_table = 'tipos_insumos'
    ordering = ['id']