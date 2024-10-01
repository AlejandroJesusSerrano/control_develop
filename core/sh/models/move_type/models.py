from django.db import models
from django.forms import model_to_dict

class Move_Type(models.Model):
  move = models.CharField(max_length = 35, verbose_name = 'Movimiento')
  details = models.CharField(max_length=150, verbose_name = 'Detalle Movimiento', blank=True, null=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return self.move

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Tipo de Movimiento'
    verbose_name_plural = 'Tipos Movimientos'
    db_table = 'tipo_movimiento'
    ordering = ['id']