from django.db import models
from django.forms import model_to_dict

from ..patchera.models import Patchera

class Patch_Port(models.Model):
  patchera = models.ForeignKey(Patchera, related_name = 'patchera_port', verbose_name = 'Patchera', on_delete = models.CASCADE)
  port = models.CharField(max_length = 2, verbose_name='Puerto')
  switch_port_in = models.OneToOneField('sh.Switch_Port', related_name='patch_port_switch_port_in', verbose_name='Puerto de Switch', on_delete=models.CASCADE, blank=True, null=True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'PUERTO: {self.port} PATCHERA: {self.patchera.patchera} DEL RACK: {self.patchera.rack.rack}'

  def toJSON(self):
    item = model_to_dict(self)
    item['patch'] = self.patchera.patchera
    item['rack'] = f'RACK: {self.patchera.rack.rack} EN OFICINA: {self.patchera.rack.office.office} / LOCALIDAD: {self.patchera.rack.office.loc.edifice.location.location} / PROVINCIA: {self.patchera.rack.office.loc.edifice.location.province.province}'
    return item

  def get_next_connection(self):
    if self.switch_port_in is not None:
      return self.switch_port_in
    return None

  class Meta:
    verbose_name = 'Puerto Patchera'
    verbose_name_plural = 'Puertos Patcheras'
    db_table = 'patchs_ports'
    ordering = ['id']
    constraints = [
        models.UniqueConstraint(fields=['patchera', 'port'], name='unique_patchera_port')
    ]