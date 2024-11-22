from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patchera

class PatcheraForm(forms.ModelForm):

  class Meta:
    model = Patchera
    fields = ['rack', 'patchera']
    widgets = {
      'rack': Select(attrs={'class': 'form-control select2'}),
      'patchera': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de la patchera'})
    }
    help_texts = {
      'patchera': '* El número de la patchera, se refiere a la posición de la misma en el Rack'
    }

  def clean(self):
    rack = self.cleaned_data.get('rack')
    patchera = self.cleaned_data.get('patchera')

    if Patchera.objects.filter(rack=rack, patchera=patchera).exists():
      self.add_error('patch', f"la posición ingresada en el rack '{rack}', ya se encuentra registrada. Ingrese una diferente")

    cleaned_data = super().clean()
    return cleaned_data