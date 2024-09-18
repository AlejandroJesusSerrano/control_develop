from django.forms import *
from django import forms
from django.forms import TextInput, Textarea

from core.sh.models import Rack

class RackForm(forms.ModelForm):

  class Meta:
    model = Rack
    fields = [
      'rack', 'details'
              ]
    widgets = {
      'rack': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el Nombre del Rack'
        }
      ),
      'details': Textarea(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese detalles que ayuden a individualizar el Rack'
        }
      )
    }
    help_texts = {
      'details': '* Aqui puede ingresar referencia de la ubicación, forma, y demas detalles que ayuden a individualizar el Rack'
    }

  def clean(self):
    rack = self.cleaned_data.get('rack').upper()

    if Rack.objects.filter(rack__iexact=rack).exists():
      self.add_error('rack', f"El Rack que se quiere ingresar, ya existe")
    cleaned_data = super().clean()
    return cleaned_data