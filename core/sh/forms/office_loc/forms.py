from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Edifice, Location, Office_Loc, Province

class Office_Loc_Form(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  location=forms.ModelChoiceField(
    queryset=Location.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Office_Loc
    fields = [
      'province', 'location', 'edifice', 'floor', 'wing'
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

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.all()
    self.fields['edifice'].queryset = Edifice.objects.none()

    if 'province' in self.data:
      try:
        province_id = int(self.data.get('province'))
        self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
      except (ValueError, TypeError):
        pass

    elif self.instance.pk:
      if self.instance.edifice and self.instance.edifice.location:
        province = self.instance.edifice.location.province
        self.fields['province'].initial = province
        self.fields['location'].queryset = Location.objects.filter(province=province)
        self.fields['location'].initial = self.instance.edifice.location

    if 'location' in self.data:
      try:
        location_id = int(self.data.get('location'))
        self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
      except (ValueError, TypeError):
        pass

    elif self.instance.pk:
      if self.instance.edifice:
        location = self.instance.edifice.location
        self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
        self.fields['edifice'].initial = self.instance.edifice

  def clean(self):
    cleaned_data = super().clean()

    edifice = self.cleaned_data.get('edifice')
    floor = self.cleaned_data.get('floor')
    wing = self.cleaned_data.get('wing').upper()

    if Office_Loc.objects.filter(edifice=edifice,floor=floor, wing=wing).exists():
      self.add_error('floor', f"Ya esta cargado el piso '{floor}' en este edificio")
      self.add_error('wing', f"Ya se encuentra registreada el ala: '{wing}', en el piso: '{floor}' de este edificio")

    return cleaned_data