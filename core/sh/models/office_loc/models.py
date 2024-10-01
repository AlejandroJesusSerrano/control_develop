from django.db import models
from django.forms import model_to_dict

from ..edifice.models import Edifice

class Office_Loc(models.Model):

  edifice = models.ForeignKey(Edifice, related_name = 'office_loc_edifice', verbose_name = 'Edificio', on_delete = models.CASCADE)
  floor = models.CharField(max_length = 2, verbose_name ='Piso')
  wing = models.CharField(max_length = 50, verbose_name = 'Ala', null=False, blank=False)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.wing = self.wing.upper()
    self.floor = self.floor.upper()
    super(Office_Loc, self).save(*args, **kwargs)

  def __str__(self):
    return f'Piso: {self.floor} / Ala: {self.wing}'

  def toJSON(self):
    item = model_to_dict(self)
    if self.edifice and self.edifice.location and self.edifice.location.province:
      item['province'] = self.edifice.location.province.province
      item['location'] = self.edifice.location.location
      item['edifice'] = self.edifice.edifice
    item['floor'] = self.floor
    item['wing'] = self.wing
    return item

  class Meta:
    verbose_name = 'Locación de Oficina'
    verbose_name_plural = 'Locaciones de Oficinas'
    db_table = 'locaciones_oficinas'
    ordering = ['id']
    constraints = [
        models.UniqueConstraint(fields=['edifice', 'floor', 'wing'], name='unique_edifice_floor_wing')
    ]