from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Edifice, Location, Province

class DependencyForm(forms.ModelForm):
  province=forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  location=forms.ModelChoiceField(
    queryset=Location.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  class Meta:
    model = Dependency
    fields = [
      'province', 'location', 'edifice', 'dependency'
    ]
    widgets = {
      'edifice': Select(
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

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()

    if 'province' in self.data:
      try:
        province_id = int(self.data.get('province'))
        self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
      except (ValueError, TypeError):
        pass

    elif self.instance.pk:
      if self.instance.edifice and self.instance.edifice.location:
        province = self.instance.edifice.location.province
        self.fields['province'].initial = province
        self.fields['location'].queryset = Location.objects.filter(province=province)
        self.fields['location'].initial = self.instance.edifice.location

    if 'location' in self.data:
      try:
        location_id = int(self.data.get('location'))
        self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
      except (ValueError, TypeError):
        pass

    elif self.instance.pk:
      if self.instance.edifice:
        location = self.instance.edifice.location
        self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
        self.fields['edifice'].initial = self.instance.edifice

  def clean(self):
    cleaned_data = super().clean()

    edifice = self.cleaned_data.get('edifice')
    dependency = self.cleaned_data.get('dependency')

    if Dependency.objects.filter(edifice=edifice, dependency=dependency).exists():
      self.add_error('dependency', f"Ya existe la dependencia '{dependency}' en la localidad y provincia seleccionadas")

    return cleaned_data