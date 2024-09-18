from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Device, Office, Brand, Dev_Type, Employee, Switch_Port, Dev_Model, Wall_Port

class DeviceForm(forms.ModelForm):

  brand = forms.ModelChoiceField(
    queryset=Brand.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  dev_type = forms.ModelChoiceField(
    queryset=Dev_Type.objects.all(),
    widget=forms.Select(attrs={'class':'form-control select2'}),
    required=False
  )

  dev_model = forms.ModelChoiceField(
    queryset=Dev_Model.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  dependency = forms.ModelChoiceField(
    queryset=Dependency.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Device
    fields = [
      'dev_model', 'connection', 'ip', 'net_name', 'dev_status', 'serial_n', 'office', 'wall_port', 'switch_port', 'employee'
    ]
    widgets = {
      'connection': Select(attrs={'class': 'form-control select2'}),
      'ip': TextInput(attrs={'class': 'form-control', 'placeholder': 'Si tuviera, ingrese la dirección ip del dispositivo'}),
      'net_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Si tuviera, ingrese el nombre de registro en la red del dispositivo'}),
      'dev_status': Select(attrs={'class': 'form-control select2'}),
      'serial_n': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie'}),
      'office': Select(attrs={'class': 'form-control select2'}),
      'wall_port': Select(attrs={'class': 'form-control select2'}),
      'switch_port': Select(attrs={'class': 'form-control select2'}),
      'employee': SelectMultiple(attrs={'class': 'form-control select2'}),
    }

  def __init__(self, *args, **kwargs):
    super(DeviceForm, self).__init__(*args, **kwargs)

    self.fields['dev_model'].queryset = Dev_Model.objects.none()
    self.fields['office'].queryset = Office.objects.none()
    self.fields['wall_port'].queryset = Wall_Port.objects.none()
    self.fields['switch_port'].queryset = Switch_Port.objects.none()
    self.fields['employee'].queryset = Employee.objects.none()

    if self.instance.pk:
      device = self.instance

      self.fields['dev_model'].queryset = Dev_Model.objects.filter(
        brand = self.instance.dev_model.brand,
        dev_type = self.instance.dev_model.dev_type
      )

      self.fields['office'].queryset = Office.objects.filter(
        dependency = self.instance.office.dependency
      )

      self.fields['wall_port'].queryset = Wall_Port.objects.filter(office=self.instance.office)
      self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office=self.instance.office)
      self.fields['employee'].queryset = Employee.objects.filter(office=self.instance.office)

    else:

      if 'dependency' in self.data:
        try:
          dependency_id = int(self.data.get('dependency'))
          self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id)
        except:
          pass

      if 'office' in self.data:
        try:
          office_id = int(self.data.get('office'))
          self.fields['wall_port'].queryset = Wall_Port.objects.filter(office_id=office_id)
          self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office_id=office_id)
          self.fields['employee'].queryset = Employee.objects.filter(office_id=office_id)
        except (ValueError, TypeError):
          pass

      if 'brand' in self.data and 'dev_type' in self.data:
        try:
          brand_id = int(self.data.get('brand'))
          dev_type_id = int(self.data.get('dev_type'))
          self.fields['dev_model'].queryset = Dev_Model.objects.filter(brand_id=brand_id, dev_type_id=dev_type_id)
        except (ValueError, TypeError):
          pass

  def clean(self):
    cleaned_data = super().clean()
    print("cleaned data: ", cleaned_data)
    return cleaned_data