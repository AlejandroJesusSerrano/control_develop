from django.forms import *
from django import forms
from django.forms import Select, TextInput, DateInput

from core.sh.models import Suply
0
class SuplyForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['serial_suply'].widget.attrs['autofocus'] = True

  class Meta:
      model = Suply
      fields = '__all__'
      widget = {
        'suply_type': Select(
          attrs={
            'placeholder': 'Seleccione el tipo de insumo'
          }
        ),
        'dev_model': Select(
          attrs={
            'placeholder': 'Seleccione para que dispositivo es el insumo'
          }
        ),
        'serial_suply': TextInput(
          attrs={
            'placeholder': 'Ingrese el número de serie del insumo'
          }
        ),
        'date_in': DateInput(
          attrs={
            'placeholder': 'Ingrese la fecha de ingreso al stock del insumo'
          }
        )
      }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data