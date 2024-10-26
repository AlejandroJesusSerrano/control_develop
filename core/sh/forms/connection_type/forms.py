from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Connection_Type

class ConnectionTypeForm(forms.ModelForm):

  class Meta:
    model = Connection_Type
    fields = '__all__'
    widgets = {
      'connection_type': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese un Tipo de Conexion'
        }
      ),
    }

  def clean(self):
    connection_type = self.cleaned_data.get('connection_type').upper()

    if Connection_Type.objects.filter(connection_type__iexact=connection_type).exists():
      self.add_error('connection_type', f"El Tipo de Conexión '{connection_type}' ya se encuentra registrado. Ingrese uno diferente")

    cleaned_data = super().clean()
    return cleaned_data