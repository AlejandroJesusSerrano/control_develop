from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Dev_Type

class Dev_TypeForm(forms.ModelForm):

  class Meta:
    model = Dev_Type
    fields = ('dev_type',)
    widgets = {
      'dev_type': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese un Tipo de Dispositivo',
          'autofocus': True,
          'id': 'dev_type_input'
        }
      ),
    }

  def clean(self):
    dev_type = self.cleaned_data.get('dev_type').upper()

    if Dev_Type.objects.filter(dev_type__iexact=dev_type).exists():
      self.add_error('dev_type', f"El tipo de desipositivo {dev_type} ya se encuentra registrado")
    cleaned_data = super().clean()
    return cleaned_data

