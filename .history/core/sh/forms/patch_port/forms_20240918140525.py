from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patch_Port

class PatchPortForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['port'].widget.attrs['autofocus'] = True

  class Meta:
    model = Patch_Port
    fields = '__all__'
    widget = {
      'patch': Select(
        attrs={
          'placeholder': 'Seleccione la Patchera'
        }
      ),
      'port': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de puerto'
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