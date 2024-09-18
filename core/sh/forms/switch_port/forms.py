from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Switch_Port

class SwitchPortForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['port_id'].widget.attrs['autofocus'] = True

  class Meta:
    model = Switch_Port
    fields = '__all__'
    widget = {
      'switch': Select(
        attrs={
          'placeholder': 'Seleccione el Switch'
        }
      ),
      'port_id': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de puerto'
        }
      ),
      'patch_port_out': Select(
        attrs={
          'placeholder': 'Seleccione el puerto de la patchera a la que sale el puerto'
        }
      ),
      'patch_port_in': Select(
        attrs={
          'placeholder': 'Seleccione el puerto de la patchera desde la que ingresa la conexion'
        }
      ),
      'switch_in': Select(
        attrs={
          'placeholder': 'Seleccione el switch padre'
        }
      ),
      'switch_out': Select(
        attrs={
          'placeholder': 'En caso de existir, seleccione el switch hijo'
        }
      ),
      'obs': Textarea(
        attrs={
          'placeholder': 'Ingrese detalles particulares, si los hubiese'
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