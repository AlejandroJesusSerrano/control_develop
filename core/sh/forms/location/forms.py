from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Location

class LocationForm(forms.ModelForm):

  class Meta:
    model = Location
    fields = ('province', 'location')
    widgets = {
      'province': Select(
        attrs={
          'class': 'form-control select2',
          'id': 'id_province',
          'autofocus': True
        }
      ),

      'location': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese una localidad',
          'id': 'id_location_input'
        }
      )
    }

  def clean(self):
    cleaned_data=super().clean()
    province = self.cleaned_data.get('province')
    location = self.cleaned_data.get('location')

    if location:
      cleaned_data['location'] = location.upper()

    if Location.objects.filter(province=province, location__iexact=location).exists():
      self.add_error('province', "La localidad ya existe asociada a la provincia seleccionada")
      self.add_error('location', "La localidad ya existe asociada a la provincia seleccionada")

    cleaned_data = super().clean()
    return cleaned_data