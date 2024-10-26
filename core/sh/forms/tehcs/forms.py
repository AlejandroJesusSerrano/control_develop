from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Techs

class TechsForm(forms.ModelForm):

  class Meta:
    model = Techs
    fields = '__all__'
    widgets = {
      'name': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el nombre del Técnico'
        }
      ),
      'last_name': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el apellido del Técnico'
        }
      )
    }

  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name').upper()
    last_name = cleaned_data.get('last_name').upper()

    if Techs.objects.filter(name=name, last_name=last_name):
      self.add_error('name', f"El nombre '{name}', ya se encuentra registrado con el apellido")
      self.add_error('last_name', f"El apellido '{last_name}', ya se encuetra registrado con el nombre")
    return cleaned_data