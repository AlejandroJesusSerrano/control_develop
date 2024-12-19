from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Move_Type

class MoveTypeForm(forms.ModelForm):

  class Meta:
      model = Move_Type
      fields = [
        'move', 'details'
      ]
      widgets = {
        'move': TextInput(
          attrs={
            'placeholder': 'Ingrese el tipo de movimiento',
            'class': 'form-control',
            'autofocus': True, 
            'id': 'id_move_input'
          }),
        'details': TextInput(
          attrs={
            'class': 'form-control',
            'placeholder': 'Agregue algún detalle específico al respecto, de ser necesario',
            'id': 'id_move_details_input'
          }
        )
      }
      help_texts = {
        'details': 'El detalle no debe superar los 150 caracteres'
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