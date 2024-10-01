from django.db import models
from django.forms import model_to_dict

from ..brands.models import Brand
from ..dev_type.models import Dev_Type

class Dev_Model(models.Model):
  dev_type = models.ForeignKey(Dev_Type, related_name = 'models_dev_type', verbose_name = 'Tipo de Dispositivo', on_delete = models.CASCADE)
  brand = models.ForeignKey(Brand, related_name = 'models_brand', verbose_name = 'Marca', on_delete = models.CASCADE)
  dev_model = models.CharField(max_length = 50, verbose_name = 'Modelo')
  image = models.ImageField(upload_to='img_models/%Y/%m/%d', null = True, blank = True, verbose_name = 'Imagen')
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.dev_model = self.dev_model.upper()
    super(Dev_Model, self).save(*args, **kwargs)

  def __str__(self):
    return self.dev_model

  def toJSON(self):
    item = model_to_dict(self)
    item['dev_type'] = self.dev_type.dev_type
    item['brand'] = self.brand.brand
    item['image'] = self.image.url if self.image else '/media/no_file.svg'
    return item

  class Meta:
    verbose_name = 'Modelo'
    verbose_name_plural = 'Modelos'
    db_table = 'modelo'
    ordering = ['id']
    constraints = [
        models.UniqueConstraint(fields=['dev_type', 'brand', 'dev_model'], name='unique_dev_type_brand_model')
    ]
