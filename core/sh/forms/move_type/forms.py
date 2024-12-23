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


  def clean(self):
    move = self.cleaned_data.get('move')

    if move and Move_Type.objects.filter(move__iexact=move).exists():
      self.add_error('move', f"El tipo de movimiento '{move}', ya se encuentra registrado. Ingrese una diferente")

    cleaned_data = super().clean()
    return cleaned_data