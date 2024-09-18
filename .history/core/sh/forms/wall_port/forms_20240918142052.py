from django.forms import *
from django import forms
from django.forms import ModelForm, Select, TextInput, Textarea, FileInput, DateInput

from core.sh.models import Connection_Type, Dependency, Dev_Status, Device, Edifice, Location, Move_Type, Movements, Office, Office_Loc, Patch_Port, Patchera, Province, Brand, Dev_Type, Employee_Status, Employee, Rack, Suply, Suply_Type, Switch_Port, Techs, Dev_Model, Wall_Port, Switch

class WallPortForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['wall_port'].widget.attrs['autofocus'] = True

  class Meta:
      model = Wall_Port
      fields = '__all__'
      widget = {
        'office': Select(
          attrs={
            'placeholder': 'Seleccione la Oficina'
          }
        ),
        'wall_port': TextInput(
          attrs={
            'placeholder': 'Ingrese el puerto/boca de la pared'
          }
        ),
        'patch_port': Select(
          attrs={
            'placeholder': 'Seleccione el puerto de la patchera de origen'
          }
        ),
        'switch_port_in': Select(
          attrs={
            'placeholder': 'En caso de ser conexion directa, seleccione el puerto del switch de origen'
          }
        ),
        'switch_out': Select(
          attrs={
            'placeholder': 'En caso de extender la boca, seleccione el switch hijo'
          }
        ),
        'details': Textarea(
          attrs={
            'placeholder': 'De ser necesario, ingrese detalles particulares'
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