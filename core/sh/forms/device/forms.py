from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Device, Office, Brand, Dev_Type, Employee, Switch_Port, Dev_Model, Wall_Port
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province

class DeviceForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  location = forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  dependency = forms.ModelChoiceField(
    queryset=Dependency.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  edifice = forms.ModelChoiceField(
    queryset=Edifice.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  loc = forms.ModelChoiceField(
    queryset=Office_Loc.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

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

  class Meta:
    model = Device
    fields = [
      'province', 'location', 'dependency', 'edifice', 'loc', 'dev_model', 'connection', 'ip', 'net_name', 'dev_status', 'serial_n', 'office', 'wall_port', 'switch_port', 'employee'
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

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.none()
    self.fields['dependency'].queryset = Dependency.objects.none()
    self.fields['loc'].queryset = Office_Loc.objects.none()
    self.fields['dev_model'].queryset = Dev_Model.objects.none()
    self.fields['office'].queryset = Office.objects.none()
    self.fields['wall_port'].queryset = Wall_Port.objects.none()
    self.fields['switch_port'].queryset = Switch_Port.objects.none()
    self.fields['employee'].queryset = Employee.objects.none()

    if self.instance.pk:
      device = self.instance

      self.fields['province'].initial = self.instance.office.loc.edifice.location.province
      selected_province = self.instance.office.loc.edifice.location.province

      self.fields['location'].queryset = Location.objects.filter(province=selected_province)
      self.fields['location'].initial = self.instance.office.loc.edifice.location
      selected_location = self.instance.office.loc.edifice.location

      self.fields['edifice'].queryset = Edifice.objects.filter(location=selected_location)
      self.fields['edifice'].initial = self.instance.office.loc.edifice
      selelcted_edifice = self.instance.office.loc.edifice

      self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location=selected_location)
      self.fields['dependency'].initial = self.instance.office.dependency

      self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=selelcted_edifice)
      self.fields['loc'].initial = self.instance.office.loc
      selected_loc = self.instance.office.loc

      self.fields['office'].queryset = Office.objects.filter(loc=selected_loc)
      self.fields['office'].initial = self.instance.office
      selected_office = self.instance.office

      self.fields['dev_model'].queryset = Dev_Model.objects.filter(
        brand = self.instance.dev_model.brand,
        dev_type = self.instance.dev_model.dev_type
      )

      self.fields['office'].queryset = Office.objects.filter(
        dependency = self.instance.office.dependency
      )

      self.fields['wall_port'].queryset = Wall_Port.objects.filter(office=selected_office)
      self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office=selected_office)
      self.fields['employee'].queryset = Employee.objects.filter(office=selected_office)
      self.initial['employee'] = [e.id for e in device.employee.all()]

    else:
      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
        except (ValueError, TypeError):
          pass
      else:
        self.fields['location'].queryset = Location.objects.none()

      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location_id=location_id)
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except (ValueError, TypeError):
          pass
      else:
        self.fields['dependency'].queryset = Dependency.objects.none()
        self.fields['edifice'].queryset = Edifice.objects.none()

      if 'edifice' in self.data:
        try:
          edifice_id = int(self.data.get('edifice'))
          self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id)
        except(ValueError, TypeError):
          pass
      else:
        self.fields['loc'].queryset = Office_Loc.objects.none()

      if 'loc' in self.data:
        try:
          loc_id = int(self.data.get('loc'))
          self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id)
        except(ValueError, TypeError):
          pass
      else:
        self.fields['office'].queryset = Office.objects.none()

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