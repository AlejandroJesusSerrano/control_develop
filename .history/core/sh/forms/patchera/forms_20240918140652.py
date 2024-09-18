from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patchera

class PatcheraForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['patch'].widget.attrs['autofocus'] = True

  class Meta:
    model = Patchera
    fields = '__all__'
    widget = {
      'rack': Select(
        attrs={
          'placeholder': 'Seleccione el Rack donde se encuentra la Patchera'
        }
      ),
      'patch': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de orden de la patchera en el rack'
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