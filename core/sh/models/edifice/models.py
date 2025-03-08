from django.db import models
from django.forms import model_to_dict

from ..location.models import Location

class Edifice(models.Model):
  location = models.ForeignKey(Location, related_name='edifice_location', on_delete = models.CASCADE, verbose_name = 'Localidad')
  edifice = models.CharField(max_length = 50, verbose_name = 'Edificio')
  address = models.TextField(verbose_name = 'Domicilio')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self,*args, **kwargs):
    self.edifice = self.edifice.upper()
    self.address = self.address.upper()
    super(Edifice, self).save(*args, **kwargs)

  def __str__(self):
    edifice_info = f"Edificio: {self.edifice} / Localidad: {self.location.location} / Provincia: {self.location.province}"
    return edifice_info

  def toJSON(self):
    item = model_to_dict(self)
    item['province'] = self.location.province.province
    item['location'] = self.location.location
    return item

  class Meta:
    verbose_name = 'Edificio'
    verbose_name_plural = 'Edificios'
    db_table = 'edificios'
    ordering = ['id']
    constraints = [
        models.UniqueConstraint(fields=['edifice', 'location'], name='unique_edifice_location'),
        models.UniqueConstraint(fields=['address', 'edifice'], name='unique_address_edifice'),
        models.UniqueConstraint(fields=['address', 'location'], name='unique_address_location')
    ]