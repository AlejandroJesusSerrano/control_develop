from django.db import models
from django.forms import model_to_dict

class Move_Type(models.Model):
  move = models.CharField(max_length = 35, verbose_name = 'Movimiento')
  details = models.CharField(max_length=150, verbose_name = 'Detalle Movimiento', blank=True, null=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.move = self.move.upper()
    self.details = self.details.upper()
    super(Move_Type, self).save(*args, **kwargs)

  def __str__(self):
    return self.move

  def toJSON(self):
    item = model_to_dict(self)
    item['move'] = self.move
    item['details'] = self.details if self.details else 'NO HAY ACLARACIONES AL RESPECTO'
    return item

  class Meta:
    verbose_name = 'Tipo de Movimiento'
    verbose_name_plural = 'Tipos Movimientos'
    db_table = 'tipo_movimiento'
    ordering = ['id']
    constraints = [
      models.UniqueConstraint(fields=['move', 'details'], name='unique_move_details')
    ]