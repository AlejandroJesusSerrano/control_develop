from django.forms import *
from django import forms
from django.forms import ModelForm, TextInput, Textarea

from core.sh.models import Connection_Type, Rack

class ConnectionTypeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['connection_type'].widget.attrs['autofocus'] = True

  class Meta:
    model = Connection_Type
    fields = '__all__'
    widget = {
      'connection_type': TextInput(
        attrs={
          'placeholder': 'Ingrese el Tipo de Conexión'
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