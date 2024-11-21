from django.db import models
from django.forms import model_to_dict

from ..office.models import Office
from ..switch_port.models import Switch_Port

class Wall_Port(models.Model):
    office = models.ForeignKey(Office, related_name='office_wall_port', verbose_name='Oficina', on_delete=models.CASCADE)
    wall_port = models.CharField(max_length=8, verbose_name='Boca Pared')
    switch_port_in = models.OneToOneField(Switch_Port, related_name='wall_switch_port_in', verbose_name='Puerto del Switch Padre', on_delete=models.CASCADE, null=True, blank=True)
    patch_port_in = models.OneToOneField(Patch_Port, related_name='switch_patch_port_in', verbose_name='Puerto de patchera de Entrada', on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name='Última Modificación')

    def __str__(self):
        switch_info = f'-> SWITCH: {self.switch_port_out.switch.brand} DE {self.switch_port_out.switch.ports_q} BOCAS EN EL PUERTO {self.switch_port_out.port_id}'  if self.switch_port_out else 'NO SWITCH'
        patch_port_in_info = f"PATCHERA: {self.switch_port_in.patch_port_out.patch} -> PUERTO: {self.switch_port_in.patch_port_out.port}" if self.switch_port_in.patch_port_out else "NO PATCH"
        patch_port_out_info = f"PATCHERA: {self.switch_port_in.patch_port_in.patch} -> PUERTO: {self.switch_port_in.patch_port_in.port}" if self.switch_port_in.patch_port_in else "NO PATCH"
        switch_port_in_info = f"SWITCH/RACK: {self.switch_port_in.switch.switch_rack_pos} -> PUERTO: {self.switch_port_in.port_id} -> RACK: {self.switch_port_in.switch.rack}" if self.switch_port_in else "NO SWITCH"
        switch_port_out_info = f"SWITCH: {self.switch_port_in.switch_out.brand} -> DE {self.switch_port_in.switch_out.ports_q} BOCAS"  if self.switch_port_in.switch_out else "NO SWITCH"
        return f'BOCA: {self.wall_port} EN OFICINA {self.office.office} -> INGRESO A LA BOCA DESDE: {patch_port_in_info} -> {switch_port_in_info} -> EXTENSION DE LA SEÑAL: {switch_info} -> {patch_port_out_info} -> {switch_port_out_info}'

    def toJSON(self):
        item = model_to_dict(self)
        item['office'] = self.office.office
        item['wall_port'] = self.wall_port
        item['switch_port_in'] = 'RACK: '+str(self.switch_port_in.switch.rack)+'-> SWITCH: '+str(self.switch_port_in.switch.switch_rack_pos)+'-> PUERTO: '+str(self.switch_port_in.port_id) if self.switch_port_in else 'NO SWITCH'
        item['switch_port_out'] = 'RACK: '+str(self.switch_port_out.switch.rack)+'-> SWITCH: '+str(self.switch_port_out.switch.switch_rack_pos)if self.switch_port_out else 'NO SWITCH'
        item['details'] = self.details if self.details else 'SIN DETALLES'
        return item

    class Meta:
        verbose_name = 'Boca Pared'
        verbose_name_plural = 'Bocas Pared'
        db_table = 'wall_port'
        ordering = ['id']