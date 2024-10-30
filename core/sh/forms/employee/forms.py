from django.forms import *
from django import forms
from django.forms import Select, TextInput, FileInput

from core.sh.models import Employee, Province, Location, Dependency, Edifice, Office_Loc, Office


class EmployeeForm(forms.ModelForm):

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

  class Meta:
    model = Employee
    fields = [
      'province', 'location', 'dependency', 'edifice', 'loc','employee_name', 'employee_last_name', 'cuil', 'status', 'user_pc', 'office', 'avatar'
    ]
    widgets = {
      'employee_name': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el Nombre del Empleado'
        }),
      'employee_last_name': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el Apellido del Empleado'}),
      'cuil': NumberInput(attrs={
        'class':'form-control',
        'placeholder': 'Ingrese el número de CUIL'
        }),
      'status': Select(attrs={'class':'form-control select2'}),
      'user_pc': TextInput(attrs={
        'class':'form-control',
        'placeholder': 'Ingrese el usurio de acceso al pc del empleado'
        }),
      'dependency': Select(attrs={'class':'form-control select2'}),
      'office': Select(attrs={'class':'form-control select2'}),
      'avatar': FileInput(attrs={'placeholder': 'Seleccione una imagen de perfil'}),
    }
    help_texts = {
      'cuil': '* Ingrese solo los numeros, sin guiones ni puntos'
    }

  def __init__(self, *args, **kwargs):
    super(EmployeeForm, self).__init__(*args, **kwargs)

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.none()
    self.fields['dependency'].queryset = Dependency.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()
    self.fields['loc'].queryset = Office_Loc.objects.none()

    if self.instance.pk:
      self.fields['province'].initial = self.instance.office.loc.edifice.location.province
      selected_province = self.instance.office.loc.edifice.location.province

      self.fields['location'].queryset = Location.objects.filter(province=selected_province)
      self.fields['location'].initial = self.instance.office.loc.edifice.location
      selected_location = self.instance.office.loc.edifice.location

      self.fields['edifice'].queryset = Edifice.objects.filter(location=selected_location)
      self.fields['edifice'].initial = self.instance.office.loc.edifice

      self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location=selected_location)
      self.fields['dependency'].initial = self.instance.office.dependency

      self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.office.loc.edifice)
      self.fields['loc'].initial = self.instance.office.loc

      self.fields['office'].queryset = Office.objects.filter(loc=self.instance.office.loc)
      self.fields['office'].initial = self.instance.office

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

  def clean(self):
    cuil = self.cleaned_data.get('cuil')
    user_pc = self.cleaned_data.get('user_pc').upper()

    if Employee.objects.filter(cuil__iexact=cuil).exists():
      self.add_error('cuil', f"El CUIL Nro: '{cuil}', ya se ecuentra asignado a un empleado. Verifique y vuelva a ingresar uno distinto")

    if Employee.objects.filter(user_pc__iexact=user_pc).exists():
      self.add_error('user_pc', f"El usuario de PC '{user_pc}', ya se encuentra vinculado a otro empleado, Verifique y vuelva a ingresar uno distinto")
    cleaned_data = super().clean()
    return cleaned_data