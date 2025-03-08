from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Edifice, Location, Province

class EdificeForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id':'id_province'}),
    required=False
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
    address =  self.cleaned_data.get('address')

    if 'location' not in cleaned_data or not location:
      self.add_error('location', 'Este campo es obligatorio')

    if 'edifice' not in cleaned_data or not edifice:
      self.add_error('edifice', 'Este campo es obligatorio')

    if 'address' not in cleaned_data or not address:
      self.add_error('address', 'Este campo es obligatorio')

    if location and edifice:

      edifice_upper = edifice.upper()
      address_upper = cleaned_data.get('address').upper()

      qs = Edifice.objects.filter(location=location, edifice=edifice_upper)
      qs_address = Edifice.objects.filter(location=location, address=address_upper)
      qs_edifice_address = Edifice.objects.filter(edifice=edifice_upper, address=address_upper)

      if self.instance.pk:
        qs = qs.exclude(pk = self.instance.pk)
        qs_address = qs_address.exclude(pk = self.instance.pk)
        qs_edifice_address = qs_edifice_address.exclude(pk = self.instance.pk)

      if  qs.exists():
        self.add_error('edifice', f"Ya existe el edificio '{edifice}' en la localidad seleccionada")

      if qs_address.exists():
        self.add_error('address', f"Ya existe la dirección '{address_upper}' en la localidad seleccionada")

      if qs_edifice_address.exists():
        self.add_error('edifice', f"Ya existe el edificio '{edifice}' con la dirección '{address_upper}'")
        self.add_error('address', f"Ya existe la dirección '{address_upper}' en el edificio '{edifice}'")

    return cleaned_data
