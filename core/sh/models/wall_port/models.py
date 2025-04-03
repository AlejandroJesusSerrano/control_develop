from django.db import models
from django.forms import model_to_dict

from ..office.models import Office

class Wall_Port(models.Model):
    office = models.ForeignKey(Office, related_name='office_wall_port', verbose_name='Oficina', on_delete=models.CASCADE)
    wall_port = models.CharField(max_length=8, verbose_name='Boca Pared')
    switch_port_in = models.OneToOneField('sh.Switch_Port', related_name='wall_switch_port_in', verbose_name='Puerto del Switch Padre', on_delete=models.CASCADE, null=True, blank=True)
    patch_port_in = models.OneToOneField('sh.Patch_Port', related_name='wall_patch_port_in', verbose_name='Puerto de patchera de Entrada', on_delete=models.CASCADE, blank=True, null=True)
    details = models.TextField(verbose_name='Observaciones', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name='Última Modificación')

    def save(self, *args, **kwargs):
        if self.wall_port:
            self.wall_port = self.wall_port.upper()
        super(Wall_Port, self).save(*args, **kwargs)

    def __str__(self):

        return f'BOCA: {self.wall_port} EN OFICINA {self.office.office}'

    def toJSON(self):
        item = model_to_dict(self)
        item['office'] = self.office.office
        item['wall_port'] = self.wall_port

        if self.switch_port_in and self.switch_port_in.switch:
            if self.switch_port_in.switch.rack:
                item['switch_port_in'] = f"RACK: {self.switch_port_in.switch.rack} -> SWITCH: {self.switch_port_in.switch.switch_rack_pos} -> PUERTO: {self.switch_port_in.port_id}"
            else:
                item['switch_port_in'] = f"SWITCH SIN RACK: {self.switch_port_in.switch.switch_rack_pos} -> PUERTO: {self.switch_port_in.port_id}"
        else:
            item['switch_port_in'] = None

        if self.patch_port_in and self.patch_port_in.patchera:
            item['patch_port_in'] = f"RACK: {self.patch_port_in.patchera.rack} -> PATCHERA: {self.patch_port_in.patchera} -> PUERTO: {self.patch_port_in.port}"
        else:
            item['patch_port_in'] = None

        item['details'] = self.details if self.details else 'SIN DETALLES'
        return item

    def get_next_connection(self):
        if self.switch_port_in is not None:
            return self.switch_port_in
        elif self.patch_port_in is not None:
            return self.patch_port_in
        return None

    class Meta:
        app_label = 'sh'
        verbose_name = 'Boca de Pared'
        verbose_name_plural = 'Bocas de Pared'
        db_table = 'wall_port'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(fields=['office', 'wall_port'], name='unique_office_wall_port'),
        ]