from django.db import models
from django.forms import model_to_dict

class Connection_Type(models.Model):
    connection_type = models.CharField(max_length = 30, verbose_name='Tipo de Conexión')
    date_creation = models.DateTimeField(auto_now = True, verbose_name = 'Fecha de Registro')
    date_updated = models.DateTimeField(auto_now_add = True, verbose_name = 'Última Modificación')

    def save(self, *args, **kwargs):
        self.connection_type = self.connection_type.upper()
        super(Connection_Type, self).save(*args, **kwargs)

    def __str__(self):
        return self.connection_type

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Conexión'
        verbose_name_plural = 'Tipos de Conexiónes'
        db_table = 'tipo_de_conexion'
        ordering = ['id']