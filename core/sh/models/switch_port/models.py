from django.db import models
from django.forms import model_to_dict

from ..patch_port.models import Patch_Port
from ..switch.models import Switch

class Switch_Port(models.Model):
  switch = models.ForeignKey(Switch, related_name = 'ports_switch', verbose_name = 'Switch', on_delete = models.CASCADE)
  port_id = models.CharField(max_length = 3, verbose_name = 'Puerto del Switch', unique=True)
  patch_port_out = models.OneToOneField(Patch_Port, related_name = 'port_patch_port_out', verbose_name= 'Puerto Patchera Salida', null = True, blank = True, on_delete = models.CASCADE)
  patch_port_in = models.OneToOneField(Patch_Port, related_name = 'port_patch_port_in', verbose_name = 'Puerto Patchera Entrada', null = True, blank = True, on_delete = models.CASCADE)
  switch_in = models.ForeignKey(Switch, related_name = 'ports_switch_in', verbose_name = 'Switch de Ingreso', null=True, blank=True, on_delete = models.CASCADE)
  switch_out = models.ForeignKey(Switch, related_name = 'ports_switch_out', verbose_name = 'Switch de Salida', null = True, blank = True, on_delete = models.CASCADE)
  obs = models.TextField(verbose_name = 'observaciones', null = True, blank = True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    return f'{self.switch.rack}  - PUERTO: {self.port_id} - EXTENSION INGRESO: {self.switch_in} - SALIDA A EXTENSION: {self.switch_out}'

  def toJSON(self):
    item = model_to_dict(self)
    item['rack'] = self.switch.rack.rack if self.switch and self.switch.rack else 'NO RACK'
    item['switch'] = str(self.switch.model.brand) +'-> '+str(self.switch.ports_q)+'-> Rack Pos: '+str(self.switch.switch_rack_pos)
    item['patch_out'] = 'SI' if self.patch_port_out else 'NO'
    item['patch_port_out'] = str(self.patch_port_out.patch.rack.rack) +' patchera: '+str(self.patch_port_out.patch.patch)+'puerto: '+str(self.patch_port_out.port) if self.patch_port_out and self.patch_port_out.patch else 'NO PATCH'
    item['patch_in'] = 'SI' if self.patch_port_in else 'NO'
    item['patch_port_in'] = str(self.patch_port_in.patch.rack.rack) +' patchera: '+str(self.patch_port_in.patch.patch)+'puerto: '+str(self.patch_port_in.port) if self.patch_port_in and self.patch_port_in.patch else 'NO PATCH'
    item['switchIn'] = 'SI' if self.switch_in else 'NO'
    item['switch_in'] = str(self.switch_in.rack.rack) +' switch: '+str(self.switch_in.switch_rack_pos) if self.switch_in and self.switch_in.rack else 'NO SWITCH'
    item['switchOut'] = 'SI' if self.switch_out else 'NO'
    item['switch_out'] = str(self.switch_out.rack.rack) +' switch: '+str(self.switch_out.switch_rack_pos) if self.switch_out and self.switch_out.rack else 'NO SWITCH'
    item['obs'] = str(self.obs) if self.obs else 'NO HAY OBSERVACIONES'
    return item

  class Meta:
    verbose_name = 'Puerto de Switch'
    verbose_name_plural = 'Puertos de Switchs'
    db_table = 'puertos_switchs'
    ordering = ['id']
