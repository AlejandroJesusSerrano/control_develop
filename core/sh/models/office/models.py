from django.db import models
from django.forms import model_to_dict

from ..dependency.models import Dependency
from ..office_loc.models import Office_Loc

class Office(models.Model):
  dependency = models.ForeignKey(Dependency, related_name = 'offices_dependencies', verbose_name = 'Dependencia', on_delete=models.CASCADE)
  loc = models.ForeignKey( Office_Loc, related_name = 'office_location', verbose_name = 'Piso/Ala', on_delete = models.CASCADE)
  office = models.CharField(max_length = 75, verbose_name = 'Oficina')
  description = models.TextField(verbose_name='Descripcion', blank=True, null=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def save(self, *args, **kwargs):
    self.office = self.office.upper()
    super(Office, self).save(*args, **kwargs)

  def __str__(self):
    return self.office

  def toJSON(self):
    item = model_to_dict(self)
    if self.loc and self.loc.edifice and self.loc.edifice.location and self.loc.edifice.location.province:
      item['province'] = self.loc.edifice.location.province.province
      item['location'] = self.loc.edifice.location.location
      item['edifice'] = self.loc.edifice.edifice
      floor_wings = Office_Loc.objects.all()
      loc_data = [
        {'floor': l.floor, 'wing': l.wing}
        for l in floor_wings
      ]
      item['loc'] = loc_data
    item['dependency'] = self.dependency.dependency
    item['office'] = self.office
    return item

  class Meta:
    verbose_name = 'Oficina'
    verbose_name_plural = 'Oficinas'
    db_table = 'oficina'
    ordering = ['id']
    constraints = [
      models.UniqueConstraint(fields=['office', 'dependency'], name = 'unique_office_dependency')
    ]