from django.db import models
from django.forms import model_to_dict

class Switch_Port(models.Model):
  switch = models.ForeignKey('sh.Switch', related_name = 'ports_switch', verbose_name = 'Switch', on_delete = models.CASCADE)
  port_id = models.CharField(max_length = 3, verbose_name = 'Puerto del Switch')
  obs = models.TextField(verbose_name = 'observaciones', null = True, blank = True)
  date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
  date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

  def __str__(self):
    if self.switch.rack:
      return f'PUERTO: {self.port_id} - SWITCH {self.switch.model.brand} / {self.switch.model.dev_model}, POSICION {self.switch.switch_rack_pos}, RACK {self.switch.rack},  OFICINA {self.switch.rack.office}'
    else:
      return f'PUERTO: {self.port_id} - SWITCH {self.switch.model.brand} / {self.switch.model.dev_model}, OFICINA {self.switch.rack.office}'

  def toJSON(self):
    item = model_to_dict(self)
    item['rack'] = self.switch.rack.rack if self.switch and self.switch.rack else 'NO RACK'
    item['switch'] = str(self.switch.model.brand) +'-> '+str(self.switch.ports_q)+'-> Rack Pos: '+str(self.switch.switch_rack_pos)
    item['obs'] = str(self.obs) if self.obs else 'NO HAY OBSERVACIONES'
    return item

  class Meta:
    verbose_name = 'Puerto de Switch'
    verbose_name_plural = 'Puertos de Switchs'
    db_table = 'puertos_switchs'
    ordering = ['id']
    constraints = [
      models.UniqueConstraint(fields=['switch', 'port_id'], name='unique_switch_port_id'),
    ]
