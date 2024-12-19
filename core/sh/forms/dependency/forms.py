from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Location, Province

class DependencyForm(forms.ModelForm):
  province = ModelChoiceField(
    queryset = Province.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
    required = False
  )

  class Meta:
    model = Dependency
    fields = [
      'province', 'location',  'dependency'
    ]

    widgets = {
      'location': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_location'
      }),

      'dependency': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese la dependencia',
        'id': 'id_dependency_input'
      }),
    }

  def __init__(self, *args, **kwargs):
    super(DependencyForm, self).__init__(*args, **kwargs)

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.all().order_by('location')

    if 'province' in self.data:
      try:
        province_id = int(self.data.get('province'))
        if province_id:
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
      except (ValueError, TypeError):
        pass

    elif self.instance.pk:
      self.fields['location'].queryset = Location.objects.all().order_by('location')

  def clean(self):
    cleaned_data = super().clean()

    location = self.cleaned_data.get('location')
    dependency = self.cleaned_data.get('dependency')

    qs = Dependency.objects.filter(location=location, dependency=dependency)
    if self.instance.pk:
      qs = qs.exclude(pk = self.instance.pk)

    if qs.exists():
      self.add_error('dependency', f"Ya existe la dependencia '{dependency}' en la localidad y provincia seleccionadas")

    return cleaned_data