from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Edifice, Location, Province

class EdificeForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id':'id_province'}),
    required=True
  )

  class Meta:
    model = Edifice
    fields = [
              'province', 'location', 'edifice', 'address'
              ]
    widgets = {
      'location': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_location'
      }),
      'edifice': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese un nombre identificatorio para el Edificio',
          'id': 'id_edifice_input'
        }),
      'address': Textarea(
        attrs={
          'class': 'form-control',
          'placeholder': 'Escriba el domiclio, en caso de tener mas de uno separar por ";"',
          'id': 'id_address_input'
        }
      )
    }

  def __init__(self, *args, **kwargs):
    super(EdificeForm, self).__init__(*args, **kwargs)

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.all()

    if self.instance.pk:

      if self.instance.location and self.instance.location.province:
        province = self.instance.location.province
        self.fields['province'].initial = province

        self.fields['location'].queryset = Location.objects.filter(province=province)
        self.fields['location'].initial = self.instance.location

    else:

      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
        except (ValueError, TypeError):
          pass

  def clean(self):
    cleaned_data = super().clean()

    location = self.cleaned_data.get('location')
    edifice = self.cleaned_data.get('edifice')

    qs = Edifice.objects.filter(location=location, edifice=edifice)

    if not edifice:
      self.add_error('edifice', "El nombre del edificio no puede estar vacío")
      return cleaned_data

    if location:
      duplicate_query = Edifice.objects.filter(
        location = location,
        edifice = edifice.upper()
      )

      if self.instance.pk:
        qs = qs.exclude(pk = self.instance.pk)

      if  qs.exists():
        self.add_error('edifice', f"Ya existe el edificio '{edifice}' en la localidad seleccionada")

    return cleaned_data
