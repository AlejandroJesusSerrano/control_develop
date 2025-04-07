from django.db import models
from django.forms import ValidationError, model_to_dict

class SwitchFont(models.Model):
    font_name = models.CharField(max_length=2, verbose_name = 'Fuente')
    switch = models.OneToOneField('sh.Switch', related_name='switch_font', verbose_name='Switch', on_delete=models.CASCADE, blank=True, null=True)
    font_status = models.CharField(max_length = 21, verbose_name = 'Estados de la Fuente', choices = (
        ('FUNCIONAL REPUESTO', 'FUNCIONAL REPUESTO'),
        ('FUNCIONAL EN RACK', 'FUNCIONAL EN RACK'),
        ('ROTA ESPERANDO ENVIO', 'ROTA ESPERANDO ENVIO'),
        ('ENVIDA EN REPARACION', 'ENVIDA EN REPARACION'),
        ), default = 'FUNCIONAL EN RACK')
    send_date = models.DateTimeField(auto_now_add = False, verbose_name = 'Fecha de Envio', null = True, blank = True)
    reception_date = models.DateTimeField(auto_now_add = False, verbose_name = 'Fecha de Recepcion', null = True, blank = True)
    date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de Registro')
    date_updated = models.DateTimeField(auto_now = True, verbose_name = 'Última Modificación')

    def __str__(self):
        result = f'FUENTE: {self.font_name} STATUS: {self.font_status}'

        if self.font_status == 'ENVIADA EN REPARACION':
            if self.send_date:
                formatted_send_date = self.send_date.strftime('%d/%m/%Y')
                result += f' EN FECHA: {formatted_send_date}'

        elif self.font_status == 'ROTA ESPERANDO ENVIO':
                result += ' | ESPERANDO FECHA DE ENVIO'

        else:
            if self.send_date and self.reception_date:
                formatted_send_date = self.send_date.strftime('%d/%m/%Y')
                result += f' EN FECHA: {formatted_send_date}'
            else:
                result += ' | SIN FECHA DE ENVIO'

            if self.reception_date and (not self.send_date or self.send_date <= self.reception_date):
                formatted_reception_date = self.reception_date.strftime('%d/%m/%Y')
                result += f' / FECHA DE RECEPECION (REPARADA): {formatted_reception_date}'
            else:
                result += ' / FECHA DE RECEPECION (REPARADA): SIN FECHA DE RECEPECION'

        return result


    def toJSON(self):
        item = model_to_dict(self)
        item['font'] = self.font_name
        item['switch'] = f"{self.switch.model.brand.brand} {self.switch.model.dev_model}" if self.switch.model.brand and self.switch.model.dev_model else 'GENÉRICO'
        item['rack'] = self.switch.rack.rack if self.switch.rack else 'SIN RACK'
        item['status'] = self.font_status
        item['send'] = self.send_date.strftime('%d/%m/%Y') if self.send_date else 'NO TIENE FECHA DE ENVIO'
        item['reception'] = self.reception_date.strftime('%d/%m/%Y') if self.reception_date else 'NO TIENE FECHA DE RECEPCION'
        return item

    class Meta:
        verbose_name = 'SwitchFont'
        verbose_name_plural = 'SwitchesFonts'
        db_table = 'fuentes de switchs'
        ordering = ['font_name']
        constraints = [
            models.UniqueConstraint(fields=['font_name', 'switch'], name='unique_switch_font')
        ]
