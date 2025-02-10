# core/sh/models/movements/models.py
from django.db import models
from django.forms import model_to_dict

from core.sh.models.switch.models import Switch
from core.sh.models.device.models import Device
from core.sh.models.move_type.models import Move_Type
from core.sh.models.suply.models import Suply
from core.sh.models.tehcs.models import Techs
from core.sh.models.employee.models import Employee
from core.sh.models.office.models import Office

class Movements(models.Model):
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Oficina')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Empleado')
    device = models.ForeignKey(Device, related_name='movement_device', verbose_name='Dispositivo', on_delete=models.CASCADE, null=True, blank=True)
    switch = models.ForeignKey(Switch, related_name='movement_switch', verbose_name='Switch', on_delete=models.CASCADE, null=True, blank=True)
    move = models.ForeignKey(Move_Type, related_name='movement_move_type', verbose_name='Movimiento', on_delete=models.CASCADE)
    techs = models.ForeignKey(Techs, related_name='movement_techs', verbose_name='Técnico', on_delete=models.CASCADE)
    date = models.DateField(auto_created=False, auto_now=False, auto_now_add=False, verbose_name='Fecha de realización')
    suply = models.ForeignKey(Suply, related_name='movement_suply', verbose_name='Insumo', on_delete=models.CASCADE, null=True, blank=True)
    detail = models.TextField(verbose_name='Detalle', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now=True, verbose_name='Fecha de Registro')
    date_updated = models.DateTimeField(auto_now_add=True, verbose_name='Última Modificación')

    def __str__(self):
        return f'{self.move} - {self.date} - {self.techs}'

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.date.strftime('%d/%m/%Y')
        item['techs'] = str(self.techs)
        item['move'] = str(self.move)
        item['office'] = self.office.office if self.office else 'SIN OFICINA'
        item['employee'] = f'{self.employee.employee_last_name}, {self.employee.employee_name}, CUIL Nro: {self.employee.cuil}' if self.employee else 'SIN EMPLEADO'
        item['device'] = f"{self.device.dev_model} / S/N: {self.device.serial_n}" if self.device else 'SIN DISPOSITIVO'
        item['switch'] = f"{self.switch.model.brand.brand} / {self.switch.model.dev_model} / S/N°: {self.switch.serial_n}" if self.switch else 'SIN SWITCH'
        item['suply'] = self.suply.suply_type.suply_type if self.suply else 'SIN INSUMO'
        item['detail'] = self.detail or ''
        return item

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        db_table = 'movimientos'
        ordering = ['id']