from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Employee_Status

class EmployeeStatusForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['status'].widget.attrs['autofocus'] = True

  class Meta:
    model = Employee_Status
    fields = '__all__'
    widgets = {
      'status': TextInput(
        attrs={
          'placehoder': 'Ingrese un Estado para los Empleados'
        }
      )
    }

  def save(self, commit=True):
    data = {}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data