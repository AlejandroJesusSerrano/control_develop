from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Location, Province

class DependencyForm(forms.ModelForm):
  province=forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  class Meta:
    model = Dependency
    fields = [
      'province', 'location', 'dependency'
    ]
    widgets = {
      'location': Select(
        attrs={
          'class': 'form-control select2'
          }),
      'dependency': TextInput(
        attrs={
          'class': 'form-control', 'placeholder': 'Ingrese la dependencia'
          }),
    }

  def __init__(self, *args, **kwargs):
    super(DependencyForm, self).__init__(*args, **kwargs)

    self.fields['province'].queryset = Province.objects.none()
    self.fields['location'].queryset = Location.objects.none()

    if self.instance.pk:
      dependency = self.instance

      if self.instance.location:
        province = self.instance.location.province
        self.fields['province'].initial = province
        self.fields['location'].queryset = Location.objects.filter(province=province)
        self.fields['location'].initial = self.instance.location

  def clean(self):
    cleaned_data = super().clean()

    location = self.cleaned_data.get('location')
    dependency = self.cleaned_data.get('dependency')

    if self.instance.pk:
      if Dependency.objects.filter(location=location, dependency=dependency).exclude(pk=self.instance.pk).exists():
        self.add_error('dependency', f"Ya existe la dependencia '{dependency}' en la localidad y provincia seleccionadas")
      else:
        if Dependency.objects.filter(location=location, dependency=dependency).exists():
          self.add_error('dependency', f"Ya existe la dependencia '{dependency}' en la localidad y provincia seleccionadas")
    else:
      self.add_error('dependency', 'El campo dependencia no puede estar vacío')
    return cleaned_data