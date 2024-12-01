from django.db import models
from django.forms import model_to_dict

from core.sh.models.location.models import Location

class Dependency(models.Model):
  location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='Localidad')
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
    item['province'] = self.location.province.province
    item['location'] = self.location.location
    item['dependency'] = self.dependency
    return item

  class Meta:
    verbose_name = 'Dependencia'
    verbose_name_plural = 'Dependencias'
    db_table = 'dependencia'
    ordering = ['id']
    constraints = [
      models.UniqueConstraint(fields=['dependency', 'location'], name='unique_dependency_location')
    ]