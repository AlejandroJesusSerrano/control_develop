from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Edifice, Location, Office_Loc, Province

class Office_Loc_Form(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
    required=False
  )

  location=forms.ModelChoiceField(
    queryset=Location.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_location'}),
    required=False
  )

  class Meta:
    model = Office_Loc
    fields = [
      'province', 'location', 'edifice', 'floor', 'wing'
    ]
    widgets = {
      'edifice': Select(attrs={
        'class': 'form-control select2',
        'id': 'edifice'
      }),
      'floor': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el Piso',
        'id': 'id_edifice_floor_input'
      }),
      'wing': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el Ala', 
        'id': 'id_edifice_wing_input'
      }),
    }

    help_texts = {
      'floor': '* Ingrese el piso ingresando 2 numeros, ej. 01, y PB para Planta baja',
      'wing': '* En caso de no haber una desigancion del ala, se recomienda ingresar el nombre de la calle a la que mira la misma'
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if self.instance.pk:
      if self.instance.edifice.location and self.instance.edifice.location.province:

        province = self.instance.edifice.location.province

        self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
        self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.edifice.location).order_by('edifice')

      if 'province' in self.data:
        try:
          province_id = int(self.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
          self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
        except (ValueError, TypeError):
          pass
      elif self.instance.pk:
        self.fields['location'].queryset = self.instance.edifice.location.province.location_set.order_by('location')

      if 'location' in self.data:
        try:
          location_id = int(self.get('location'))
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
        except (ValueError, TypeError):
          pass
      elif self.instance.pk:
        self.fields['edifice'].queryset = self.instance.edifice.location.edifice_location.order_by('edifice')

  def clean(self):
    cleaned_data = super().clean()

    edifice = self.cleaned_data.get('edifice')
    floor = self.cleaned_data.get('floor')
    wing = self.cleaned_data.get('wing')

    if Office_Loc.objects.filter(edifice=edifice, floor=floor, wing=wing).exists():
      self.add_error('floor', f"Ya esta cargado el piso '{floor}' en este edificio")
      self.add_error('wing', f"Ya se encuentra registreada el ala: '{wing}', en el piso: '{floor}' de este edificio")

    return cleaned_data