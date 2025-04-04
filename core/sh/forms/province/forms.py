from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Province

class ProvinceForm(forms.ModelForm):

  class Meta:
    model = Province
    fields = '__all__'
    widgets = {
      'number_id': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el número correspondiente al Distrito',
          'autofocus': True,
          'id': 'id_province_number'
        }
      ),

      'province': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': ' Ingrese el nombre del Distrito',
          'id': 'id_province_input'
        }
      )
    }
    help_texts = {
      'number_id': '* Ingrese los dos digitos identificatorios de la provincia, Ej: 04 para "CÓRDOBA" 0 17 para "SALTA"'
    }

  def clean(self):
    number_id = self.cleaned_data.get('number_id')
    province = self.cleaned_data.get('province').upper()

    qs = Province.objects.all()
    if self.instance:
      qs = qs.exclude(pk=self.instance.pk)

    if qs.filter(number_id__iexact=number_id).exists():
      self.add_error('number_id', "El id de provincia ya se encuentra registrado")

    if qs.filter(province__iexact=province).exists():
      self.add_error('province', "La provincia ya se encuentra registrada")

    cleaned_data = super().clean()
    return cleaned_data