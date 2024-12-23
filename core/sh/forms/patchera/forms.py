from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patchera
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.province.models import Province

class PatcheraForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget=Select(attrs={
      'class': 'form-control select2',
      'id': 'id_province'
    })
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget=Select(attrs={
      'class': 'form-control select2',
      'id': 'id_location'
    })
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = Select(attrs={
      'class': 'form-control select2',
      'id': 'id_edifice'
    })
  )

  class Meta:
    model = Patchera
    fields = [
      'rack', 'patchera'
    ]
    widgets = {
      'rack': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_rack'
      }),
      'patchera': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el número de la patchera',
        'id': 'id_patchera_input'
      })
    }
    help_texts = {
      'patchera': '* El número de la patchera, se refiere a la posición de la misma en el Rack'
    }

  def clean(self):
    rack = self.cleaned_data.get('rack')
    patchera = self.cleaned_data.get('patchera')

    if Patchera.objects.filter(rack=rack, patchera=patchera).exists():
      self.add_error('patchera', f"la posición ingresada en el rack '{rack}', ya se encuentra registrada. Ingrese una diferente")

    cleaned_data = super().clean()
    return cleaned_data