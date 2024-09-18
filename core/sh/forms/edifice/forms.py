from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Edifice, Location, Province

class EdificeForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  class Meta:
    model = Edifice
    fields = [
              'province','location', 'edifice', 'address'
              ]
    widgets = {
      'location': Select(attrs={'class': 'form-control select2'}),
      'edifice': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese un nombre identificatorio para el Edificio'
        }),
      'address': Textarea(
        attrs={
          'class': 'form-control',
          'placeholder': 'Escriba el domiclio, en caso de tener mas de uno separar por ";"'
        }
      )
    }

  def __init__(self, *args, **kwargs):
    super(EdificeForm, self).__init__(*args, **kwargs)

    self.fields['location'].queryset = Location.objects.all()

    if self.instance.pk:
      edifice = self.instance

      province = self.instance.location.province
      self.fields['location'].queryset = Location.objects.filter(edfice_location__province=province)
      self.fields['location'].initial = self.instance.location

  def clean(self):
    edifice = self.cleaned_data.get('edifice').upper()
    location = self.cleaned_data.get('location')

    if Edifice.objects.filter(location=location, edifice=edifice).exists():
      self.add_error('edifice', f"Ya existe el edificio '{edifice}' en la localidad seleccionada")
    cleaned_data = super().clean()
    return cleaned_data
