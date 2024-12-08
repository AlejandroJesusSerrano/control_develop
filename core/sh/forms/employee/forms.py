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
      'employee_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Nombre del Empleado'}),
      'employee_last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el Apellido del Empleado'}),
      'cuil': NumberInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el número de CUIL'}),
      'status': Select(attrs={'class':'form-control select2'}),
      'user_pc': TextInput(attrs={'class':'form-control', 'placeholder': 'Ingrese el usurio de acceso al pc del empleado'}),
      'dependency': Select(attrs={'class':'form-control select2'}),
      'office': Select(attrs={'class':'form-control select2'}),
      'avatar': FileInput(attrs={'placeholder': 'Seleccione una imagen de perfil'}),
    }
    help_texts = {
      'cuil': '* Ingrese solo los numeros, sin guiones ni puntos'
    }

  def __init__(self, *args, **kwargs):
    super(EmployeeForm, self).__init__(*args, **kwargs)

    if self.instance.pk:
      if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice and self.instance.office.loc.edifice.location and self.instance.office.loc.edifice.location.province and self.instance.office.dependency and self.instance.office.dependency.location:

        province = self.instance.office.loc.edifice.location.province
        dependency = self.instance.office.dependency
        location = self.instance.office.loc.edifice.location
        edifice = self.instance.office.loc.edifice
        loc = self.instance.office.loc

        self.initial['province'] = province.id
        self.initial['location'] = location.id
        self.initial['dependency'] = dependency.id
        self.initial['edifice'] = edifice.id
        self.initial['loc'] = loc.id
        self.initial['office'] = self.instance.office.id

        self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
        self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.office.loc.edifice.location).order_by('edifice')
        self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.office.dependency.location).order_by('dependency')
        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.office.loc.edifice).order_by('office_location')
        self.fields['office'].queryset = Office.objects.filter(loc=self.instance.office.loc, dependency=self.instance.office.dependency).order_by('office')

        if 'province' in self.data:
          try:
            province_id = int(self.data.get('province'))
            self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
            self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
            self.fields['dependency'].queryet = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('office_location')
            self.fields['office'].queryset = Office.objects.filter(
              loc__edifice__location__province_id=province_id,
              dependency__location__province_id=province_id
              ).order_by('office')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['location'].queryset = self.instance.office.loc.edifice.location.province.location_set.order_by('location')

        if 'location' in self.data:
          try:
            location_id = int(self.data.get('location'))
            self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
            self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id).order_by('dependency')
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=location_id).order_by('office_location')
            self.fields['office'].queryset = Office.objects.filter(
              loc__edifice__location_id=location_id,
              dependency__location_id=location_id
            ).order_by('office')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_location.order_by('edifice')
          self.fields['dependency'].queryset = self.instance.office.dependency.location.dependency_location.order_by('dependency')

        if 'dependency' in self.data:
          try:
            dependency_id = int(self.data.get('dependency'))
            self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id).order_by('office')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['office'].queryset = self.instance.office.dependency.offices_dependencies.order_by('office')

        if 'edifice' in self.data:
          try:
            edifice_id = int(self.data.get('edifice'))
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice_id).order_by('office_location')
            self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=edifice_id).order_by('office')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_edifice.order_by('office_location')

        if 'loc' in self.data:
          try:
            loc_id = int(self.data.get('loc'))
            self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id).order_by('office')
          except (ValueError, TypeError):
              pass
        elif self.instance.pk:
          self.fields['office'].queryset = self.instance.office.loc.office_location.order_by('office')

  def clean(self):
    cuil = self.cleaned_data.get('cuil')
    user_pc = self.cleaned_data.get('user_pc').upper()

    if Employee.objects.filter(cuil__iexact=cuil).exists():
      self.add_error('cuil', f"El CUIL Nro: '{cuil}', ya se ecuentra asignado a un empleado. Verifique y vuelva a ingresar uno distinto")

    if Employee.objects.filter(user_pc__iexact=user_pc).exists():
      self.add_error('user_pc', f"El usuario de PC '{user_pc}', ya se encuentra vinculado a otro empleado, Verifique y vuelva a ingresar uno distinto")
    cleaned_data = super().clean()
    return cleaned_data