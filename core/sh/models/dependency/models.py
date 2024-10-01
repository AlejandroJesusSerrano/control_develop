from django.db import models
from django.forms import model_to_dict

from ..edifice.models import Edifice

class Dependency(models.Model):
  edifice = models.ForeignKey(Edifice, on_delete=models.CASCADE, verbose_name='Edificio')
  dependency = models.CharField(max_length = 75, verbose_name = 'Dependencia')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.dependency = self.dependency.upper()
    super(Dependency, self).save(*args, **kwargs)

  def __str__(self):
    return self.dependency

  def toJSON(self):
    item = model_to_dict(self)
    item['province'] = self.edifice.location.province.province
    item['location'] = self.edifice.location.location
    item['edifice'] = self.edifice.edifice
    item['dependency'] = self.dependency
    return item

  class Meta:
    verbose_name = 'Dependencia'
    verbose_name_plural = 'Dependencias'
    db_table = 'dependencia'
    ordering = ['id']
    unique_together = ('edifice', 'dependency')