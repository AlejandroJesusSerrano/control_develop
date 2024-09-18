from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Edifice, Location, Office, Brand, Rack, Dev_Model, Switch

class SwitchForm(forms.ModelForm):
  brand=forms.ModelChoiceField(
    queryset=Brand.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  model=forms.ModelChoiceField(
    queryset=Dev_Model.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  location=forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  dependency=forms.ModelChoiceField(
    queryset=Dependency.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  edifice=forms.ModelChoiceField(
    queryset=Edifice.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  class Meta:
    model = Switch
    fields = [
      'brand', 'model', 'serial_n', 'ports_q', 'rack', 'switch_rack_pos', 'office', 'dependency', 'edifice', 'location'
      ]
    widgets = {
      'serial_n': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie'}),
      'ports_q': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad de puertos del Switch'}),
      'rack': Select(attrs={'class': 'form-control select2'}),
      'switch_rack_pos': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la posición del Switch en el Rack'}),
      'office': Select(attrs={'class': 'form-control select2'}),
      'dependency': Select(attrs={'class': 'form-control select2'}),
      'edifice': Select(attrs={'class': 'form-control select2'}),
      'location': Select(attrs={'class': 'form-control select2'})
    }
    help_texts = {
      'ports_q': '* Ingrese solo números',
      'switch_rack_pos': '* Ingrese el número de posición del switch en el rack'
    }

  def __init__(self, *args, **kwargs):
    super(SwitchForm, self).__init__(*args, **kwargs)

    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['model'].queryset = Dev_Model.objects.all()
    self.fields['office'].queryset = Office.objects.all()
    self.fields['dependency'].queryset = Dependency.objects.all()
    self.fields['edifice'].queryset = Edifice.objects.all()
    self.fields['location'].queryset = Location.objects.all()
    self.fields['rack'].queryset = Rack.objects.all()

    if self.instance.pk:
      switch = self.instance

      dev_type = self.instance.model.dev_type
      self.fields['brand'].queryset = Brand.objects.filter(models_brand__dev_type=dev_type).distinct()
      self.fields['brand'].initial = self.instance.model.brand

      if self.instance.model:
        self.fields['model'].queryset = Dev_Model.objects.filter(
        dev_type = dev_type,
        brand = self.instance.model.brand
      )

      if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice:
        location = self.instance.office.loc.edifice.location
        self.fields['location'].initial = location
        self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
        self.fields['edifice'].initial = self.instance.office.loc.edifice

      if self.instance.office:
        location = self.instance.office.loc.edifice.location
        self.fields['dependency'].queryset = Dependency.objects.filter(location=location)
        self.fields['dependency'].initial = self.instance.office.dependency
        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice = self.instance.office.loc.edifice,
          dependency = self.instance.office.dependency
        )
        self.fields['office'].initial = self.instance.office

  def clean(self):
    cleaned_data = super().clean()
    model = self.cleaned_data.get('model')
    serial_n = self.cleaned_data.get('serial_n')
    rack = self.cleaned_data.get('rack')
    switch_rack_pos = self.cleaned_data.get('switch_rack_pos')

    if Switch.objects.filter(model=model, serial_n=serial_n).exists():
      self.add_error('model', f"Ya se encuentra cargado este modelo de Switch")
      self.add_error('serial_n', f"El número de serie ya se encuentra registrado y asociado al mismo modelo")
    if Switch.objects.filter(rack=rack, switch_rack_pos=switch_rack_pos).exists():
      self.add_error('rack', f"El switch ya se encuentra en el Rack seleccionado")
      self.add_error('switch_rack_pos', f"La posicion seleccionada en el Rack, ya se encuentra ocupada")
    return cleaned_data