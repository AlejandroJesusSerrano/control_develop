from django.forms import *
from django import forms
from django.forms import ModelForm, Select, TextInput, Textarea, FileInput, DateInput

from core.sh.models import Connection_Type, Dependency, Dev_Status, Device, Edifice, Location, Move_Type, Movements, Office, Office_Loc, Patch_Port, Patchera, Province, Brand, Dev_Type, Employee_Status, Employee, Rack, Suply, Suply_Type, Switch_Port, Techs, Dev_Model, Wall_Port, Switch

class SuplyTypeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['suply_type'].widget.attrs['autofocus'] = True

  class Meta:
      model = Suply_Type
      fields = '__all__'
      widget = {
        'suply_type': TextInput(
          attrs={
            'placeholder': 'Ingrese el tipo de insumo'
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