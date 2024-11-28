from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Suply
from core.sh.models.brands.models import Brand
from core.sh.models.dev_model.models import Dev_Model

class SuplyForm(forms.ModelForm):

  brand = forms.ModelChoiceField(
    queryset = Brand.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  class Meta:
    model = Suply
    fields = [
      'brand', 'suply_type', 'dev_model', 'serial_suply', 'date_in'
    ]
    widgets = {
      'suply_type': Select(attrs = {'class': 'form-control select2'}),
      'dev_model': Select(attrs = {'class': 'form-control select2'}),
      'serial_suply': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie del insumo'}),
      'date_in': TextInput(attrs={'class': 'form-control', 'placeholder': 'Seleccione una fecha'}),
    }

  def __init__(self, *args, **kwargs):
    super(SuplyForm, self).__init__(*args, **kwargs)

    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['dev_model'].queryset = Dev_Model.objects.filter(dev_type__dev_type='IMPRESORA')
    self.fields['date_in'].input_formats = ['%d/%m/%Y']

  def clean(self):
    cleaned_data = super().clean()

    suply_type = cleaned_data.get('suply_type')
    dev_model = cleaned_data.get('dev_model')
    serial_suply = cleaned_data.get('serial_suply')

    if Suply.objects.filter(suply_type=suply_type, dev_model=dev_model, serial_suply=serial_suply):
      self.add_error('serial_suply', f"Ya se encuentra registrado un suministro con el tipo: '{suply_type}', para la impresora: '{dev_model}' con el S/N°: '{serial_suply}'")
    return cleaned_data

