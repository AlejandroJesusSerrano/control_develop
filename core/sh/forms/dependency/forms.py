from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Location, Province

class DependencyForm(forms.ModelForm):

  province=forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Dependency
    fields = [
      'location', 'dependency'
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

    self.fields['location'].queryset = Location.objects.none()

    if self.instance.pk:
      dependency = self.instance

      self.fields['location'].queryset = Location.objects.filter(
        province = self.instance.location.province
      )

    else:

      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
        except:
          pass

  def clean(self):
    location = self.cleaned_data.get('location')
    dependency = self.cleaned_data.get('dependency')

    if Dependency.objects.filter(location=location, dependency=dependency).exists():
      self.add_error('dependency', f"Ya existe una dependencia con los datos ingresados")
    cleaned_data = super().clean()
    return cleaned_data