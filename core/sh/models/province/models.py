from django.db import models
from django.forms import model_to_dict

class Province(models.Model):
  number_id = models.CharField(max_length = 2, verbose_name = 'Numero de Distrito', unique=True)
  province = models.CharField(max_length = 50, verbose_name = 'Nombre de Provincia', unique=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self,*args, **kwargs):
    self.province = self.province.upper()
    super(Province, self).save(*args, **kwargs)

  def __str__(self):
    return self.province

  def toJSON(self):
    item = model_to_dict(self)
    item['province'] = self.province
    item['number_id'] = self.number_id
    return item

  class Meta:
    verbose_name = 'Provincia'
    verbose_name_plural = 'Provincias'
    db_table = 'provincias'
    ordering = ['id']