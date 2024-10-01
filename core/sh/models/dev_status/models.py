from django.db import models
from django.forms import model_to_dict

class Dev_Status(models.Model):
  dev_status = models.CharField(max_length = 33, verbose_name = 'Estado del Dispositivo')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Regilstro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.dev_status = self.dev_status.upper()
    super(Dev_Status, self).save(*args, **kwargs)

  def __str__(self):
    return self.dev_status

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Estado del Dispositivo'
    verbose_name_plural = 'Estados de los Dispositivos'
    db_table = 'estado_del_dispositivo'
    ordering = ['id']