from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Edifice, Location, Office_Loc

class Office_Loc_Form(forms.ModelForm):

  location=forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Office_Loc
    fields = [
      'edifice', 'floor', 'wing'
    ]
    widgets = {
      'edifice': Select(
        attrs={
          'class': 'form-control select2'
          }),
      'floor': TextInput(
        attrs={
          'class': 'form-control', 'placeholder': 'Ingre el Piso'
          }),
      'wing': TextInput(
        attrs={
          'class': 'form-control', 'placeholder': 'Ingrese el Ala'
          }),
    }
    help_texts = {
      'floor': '* Ingrese el piso ingresando 2 numeros, ej. 01, y PB para Planta baja',
      'wing': '* En caso de no haber una desigancion del ala, se recomienda ingresar el nombre de la calle a la que mira la misma'
    }

  def __init__(self, *args, **kwargs):
    super(Office_Loc_Form, self).__init__(*args, **kwargs)

    self.fields['edifice'].queryset = Edifice.objects.none()

    if self.instance.pk:
      office_loc = self.instance

      self.fields['edifice'].queryset = Edifice.objects.filter(
        location = self.instance.edifice.location
      )

    else:

      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except:
          pass

  def clean(self):
    edifice = self.cleaned_data.get('edifice')
    location = edifice.location if edifice else None
    floor = self.cleaned_data.get('floor')
    wing = self.cleaned_data.get('wing').upper()

    if Office_Loc.objects.filter(edifice=edifice, edifice__location=location, floor=floor, wing=wing).exists():
      self.add_error('floor', f"Ya existe un registro con los datos que intenta cargar")
      self.add_error('wing', f"Ya existe un registro con los datos que intenta cargar")
    cleaned_data = super().clean()
    return cleaned_data