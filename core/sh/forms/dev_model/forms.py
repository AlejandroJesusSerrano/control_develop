from django.forms import *
from django import forms
from django.forms import ModelForm, Select, TextInput, Textarea, FileInput, DateInput

from core.sh.models import Dev_Model

class Dev_ModelForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['dev_model'].widget.attrs['autofocus'] = True

  class Meta:
    model = Dev_Model
    fields = '__all__'
    widget = {
      'dev_type': Select(
        attrs={
          'placeholder': 'Seleccione un Tipo de Dispositivo'
        }
      ),
      'brand': Select(
        attrs={
          'placeholder': 'Seleccione una Marca'
        }
      ),
      'dev_model': TextInput(
        attrs={
          'placeholder': 'Ingrese el Modelo'
        }
      ),
      'image': FileInput(
        attrs={
          'placeholder': 'Seleccione una imagen del dispositivo'
        }
      ),
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if self.is_valid():
        self.instance = super().save(commit=commit)
        data = self.instance.toJSON()
      else:
        data['error'] = self.errors.as_json()
    except Exception as e:
      data['error'] = str(e)
    return data