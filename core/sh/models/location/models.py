from django.db import models
from django.forms import model_to_dict

from ..province.models import Province

class Location(models.Model):
  province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name = 'Provincia')
  location = models.CharField(max_length = 75, verbose_name = 'Localidad')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.location = self.location.upper()
    super(Location, self).save(*args, **kwargs)

  def __str__(self):
    return self.location

  def toJSON(self):
    item = model_to_dict(self)
    item['province'] = self.province.province
    return item

  class Meta:
    verbose_name = 'Localidad'
    verbose_name_plural = 'Localidades'
    db_table = 'localidades'
    ordering = ['id']
    unique_together = ('province', 'location')