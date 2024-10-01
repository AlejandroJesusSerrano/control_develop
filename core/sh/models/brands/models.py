
from django.db import models
from django.forms import model_to_dict

class Brand(models.Model):
  brand = models.CharField(max_length=50, verbose_name = 'Marca', unique=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Regilstro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self,*args, **kwargs):
    self.brand = self.brand.upper()
    super(Brand, self).save(*args, **kwargs)

  def __str__(self):
    return self.brand

  def toJSON(self):
    item = model_to_dict(self)
    return item

  class Meta:
    verbose_name = 'Marca'
    verbose_name_plural = 'Marcas'
    db_table = 'marca'
    ordering = ['brand']