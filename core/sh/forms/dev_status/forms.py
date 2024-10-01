from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Dev_Status

class Dev_StatusForm(forms.ModelForm):

  class Meta:
    model = Dev_Status
    fields = ('dev_status',)
    widgets = {
      'dev_status': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese un Estado para el Dispositivo'
        }
      ),
    }

  def clean(self):
    dev_status = self.cleaned_data.get('dev_status')

    if Dev_Status.objects.filter(dev_status__iexact=dev_status).exists():
      self.add_error('dev_status', f"El estado de dispoditivo: {dev_status}, ya se encuentra registrado")
      cleaned_data = super().clean()
      return cleaned_data