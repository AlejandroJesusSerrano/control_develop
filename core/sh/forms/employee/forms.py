from django.forms import *
from django import forms
from django.forms import Select, TextInput, FileInput

from core.sh.models import Employee

class EmployeeForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['employee_name'].widget.attrs['autofocus'] = True

  class Meta:
    model = Employee
    fields = '__all__'
    widget = {
      'employee_name': TextInput(
        attrs={
          'placeholder': 'Ingrese el Nombre del Empleado'
        }
      ),
      'employee_last_name': TextInput(
        attrs={
          'placeholder': 'Ingrese el Apellido del Empleado'
        }
      ),
      'cuil': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de CUIL'
        }
      ),
      'status': Select(
        attrs={
          'placeholder': 'Seleccione un estado'
        }
      ),
      'user_status': Select(
        attrs={
          'placeholder': 'Ingrese el usuario del empleado'
        }
      ),
      'dependency': Select(
        attrs={
          'placeholder': 'Seleccione la dependencia a la que pertenece'
        }
      ),
      'office': Select(
        attrs={
          'placeholder': 'Seleccione la oficina en que trabaja el empleado'
        }
      ),
      'avatar': FileInput(
        attrs={
          'placeholder': 'Seleccione una imagen de perfil'
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