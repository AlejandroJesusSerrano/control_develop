from django.forms import *
from django import forms
from django.forms import ModelForm, Select, Textarea, DateInput

from core.sh.models import Movements

class MovementsForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['port_id'].widget.attrs['autofocus'] = True

  class Meta:
      model = Movements
      fields = '__all__'
      widget = {
        'device': Select(
          attrs={
            'placeholder': 'Seleccione un dispositivo'
          }
        ),
        'port_id': Select(
          attrs={
            'placeholder': 'Seleccione el tipo de movimiento'
          }
        ),
        'techs': Select(
          attrs={
            'placeholder': 'Seleccione el Técnico responsable del movimiento'
          }
        ),
        'date': DateInput(
          attrs={
            'placeholder': 'Ingrese la fecha del movimiento'
          }
        ),
        'suply': Select(
          attrs={
            'placeholder': 'En caso de haberse requerido, ingrese el insumo utilizado'
          }
        ),
        'detail': Textarea(
          attrs={
            'placeholder': 'Describa el detalle del movimiento realizado'
          }
        ),
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

