from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Employee_Status

class EmployeeStatusForm(forms.ModelForm):

  class Meta:
    model = Employee_Status
    fields = '__all__'
    widgets = {
      'status': TextInput(
        attrs={
          'class': 'form-control',
          'placehoder': 'Ingrese un Estado para los Empleados'
        }
      )
    }

  def clean(self):
    status = self.cleaned_data.get('status').upper()
    if Employee_Status.objects.filter(status__iexact=status).exists():
      self.add_error('status', f"El Estado de Dispositivo '{status}', ya se encuentra registrado. Ingrese uno diferente")

    cleaned_data=super().clean()
    return cleaned_data