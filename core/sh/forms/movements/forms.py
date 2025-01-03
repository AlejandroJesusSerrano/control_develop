from django.forms import *
from django.forms import ModelForm, Select, Textarea, DateInput

from core.sh.models.movements.models import Movements


class MovementsForm(ModelForm):

  class Meta:
      model = Movements
      fields = '__all__'
      widget = {
        'device': Select(
          attrs={
            'class': 'form-control select2',
            'id': 'id_device'
          }
        ),

        'switch': Select(
          attrs={
            'class': 'form-control select2'
          }
        ),

        'port_id': Select(
          attrs={
            'placeholder': 'Seleccione el tipo de movimiento',
            'id': 'id_port_id_input'
          }
        ),
        'techs': Select(
          attrs={
            'placeholder': 'Seleccione el Técnico responsable del movimiento',
            'id': 'id_techs'
          }
        ),
        'date': DateInput(
          attrs={
            'placeholder': 'Ingrese la fecha del movimiento',
            'id': 'id_move_date_input'
          }
        ),
        'suply': Select(
          attrs={
            'placeholder': 'En caso de haberse requerido, ingrese el insumo utilizado',
            'id': 'id_suply'
          }
        ),
        'detail': Textarea(
          attrs={
            'placeholder': 'Describa el detalle del movimiento realizado',
            'id': 'id_detail_move_input'
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

