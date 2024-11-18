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
    self.fields['location'].queryset = Location.objects.all()
    self.fields['dependency'].queryset = Dependency.objects.all()
    self.fields['loc'].queryset = Office_Loc.objects.all()
    self.fields['dev_model'].queryset = Dev_Model.objects.all()
    self.fields['office'].queryset = Office.objects.all()
    self.fields['wall_port'].queryset = Wall_Port.objects.all()
    self.fields['switch_port'].queryset = Switch_Port.objects.all()
    self.fields['employee'].queryset = Employee.objects.all()

    if self.instance.pk:

      self.initial['province'] = self.instance.office.loc.edifice.location.province
      self.initial['location'] = self.instance.office.loc.edifice.location
      self.initial['dependency'] = self.instance.office.dependency
      self.initial['edifice'] = self.instance.office.loc.edifice
      self.initial['loc'] = self.instance.office.loc
      self.initial['office'] = self.instance.office
      self.initial['brand'] = self.instance.dev_model.brand
      self.initial['dev_type'] = self.instance.dev_model.dev_type
      self.initial['dev_model'] = self.instance.dev_model
      self.initial['employee'] = [e.id for e in self.instance.employee.all()]

      self.fields['dev_model'].queryset = Dev_Model.objects.filter(
        brand = self.instance.dev_model.brand,
        dev_type = self.instance.dev_model.dev_type
      )

      self.fields['wall_port'].queryset = Wall_Port.objects.filter(office = self.instance.office)
      self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office = self.instance.office)

      self.fields['employee'].queryset = Employee.objects.filter(office=self.instance.office)

    else:
      selected_province = self.data.get('province')
      selected_location = self.data.get('location')
      selected_dependency = self.data.get('dependency')
      selected_edifice = self.data.get('edifice')
      selected_loc = self.data.get('loc')
      selected_office = self.data.get('office')
      selected_brand = self.data.get('brand')
      selected_dev_type = self.data.get('dev_type')

      try:
        selected_province = int(selected_province) if selected_province else None
      except (ValueError, TypeError):
        selected_province = None

      try:
        selected_location = int(selected_location) if selected_location else None
      except (ValueError, TypeError):
        selected_location = None

      try:
        selected_dependency = int(selected_dependency) if selected_dependency else None
      except (ValueError, TypeError):
        selected_dependency = None

      try:
        selected_edifice = int(selected_edifice) if selected_edifice else None
      except (ValueError, TypeError):
        selected_edifice = None

      try:
        selected_loc = int(selected_loc) if selected_loc else None
      except (ValueError, TypeError):
        selected_loc = None

      try:
        selected_office = int(selected_office) if selected_office else None
      except (ValueError, TypeError):
        selected_office = None

      try:
        selected_brand = int(selected_brand) if selected_brand else None
      except (ValueError, TypeError):
        selected_brand = None

      try:
        selected_dev_type = int(selected_dev_type) if selected_dev_type else None
      except (ValueError, TypeError):
        selected_dev_type = None

      office_filters = {}
      if selected_province:
        office_filters['loc__edifice__location__province_id'] = selected_province
      if selected_location:
        office_filters['loc__edifice__location_id'] = selected_location
      if selected_edifice:
        office_filters['loc__edifice_id'] = selected_edifice
      if selected_loc:
        office_filters['loc_id'] = selected_loc
      if selected_dependency:
        office_filters['dependency_id'] = selected_dependency

      self.fields['office'].queryset = Office.objects.filter(**office_filters).distinct()

      dev_model_filters = {}
      if selected_brand:
        dev_model_filters['brand_id'] = selected_brand
      if selected_dev_type:
        dev_model_filters['dev_type_id'] = selected_dev_type

      self.fields['dev_model'].queryset = Dev_Model.objects.filter(**dev_model_filters).distinct()

      if selected_office:
        self.fields['wall_port'].queryset = Wall_Port.objects.filter(office_id=selected_office)
        self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office_id = selected_office)
        self.fields['employee'].queryset = Employee.objects.filter(office_id = selected_office)

      else:
        self.fields['wall_port'].queryset = Wall_Port.objects.all()
        self.fields['switch_port'].queryset = Switch_Port.objects.all()
        self.fields['employee'].queryset = Employee.objects.all()

  def clean(self):
    cleaned_data = super().clean()
    return cleaned_data