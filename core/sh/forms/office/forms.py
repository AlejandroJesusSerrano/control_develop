from django.forms import * 
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Dependency, Edifice, Location, Office, Office_Loc, Province

class OfficeForm(forms.ModelForm):
  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control selct2'}),
    required=True
  )

  location=forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  edifice=forms.ModelChoiceField(
    queryset=Edifice.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )


  class Meta:
    model = Office
    fields = [
      'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'description'
      ]
    widgets = {
      'edifice': Select(attrs={'class': 'form-control select2'}),
      'dependency': Select(attrs={'class': 'form-control select2'}),
      'loc': Select(attrs={'class': 'form-control select2'}),
      'office': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre identificatorio para la Oficina'}),
      'description': Textarea(attrs={'class':'form-control', 'placeholder': 'Ingrese una descripción de la oficina'})
    }
    help_texts = {
      'description': '* Esta campo no es obligatorio, pero puede agregar detalles para individualizar la oficina, o agregar algún dato relevenate de la misma.'
    }

  def __init__(self, *args, **kwargs):
    super(OfficeForm, self).__init__(*args, **kwargs)

    self.fields['province'].queryset = Province.objects.all()
    self.fields['dependency'].queryset = Dependency.objects.none()
    self.fields['loc'].queryset = Office_Loc.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()
    self.fields['location'].queryset = Location.objects.none()

    if self.instance.pk:
      self.fields['province'].initial = self.instance.loc.edifice.location.provice
      selected_province = self.instance.loc.edifice.location.province

      self.fields['location'].queryset = Location.objects.filter(province=selected_province)
      self.fields['location'].initial = self.instance.loc.edifice.location
      selected_location = self.instance.loc.edifice.location

      self.fields['dependency'].queryset = Dependency.objects.filter(location = selected_location)
      self.fields['dependency'].initial = self.instance.dependency

      self.fields['edifice'].queryset = Edifice.objects.filter(location = selected_location)
      self.fields['edifice'].initial = self.instance.loc.edifice

      self.fields['loc'].queryset = Office_Loc.objects.filter(edifice = self.instance.loc.edifice)
      self.fields['loc'].initial = self.instance.loc

    else:
      if 'province' in self.data:
        try:


      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id)
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except:
          pass

      if 'edifice'in self.data:
        try:
          edifice_id = int(self.data.get('edifice'))
          self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id)
        except:
          pass

  def clean(self):
    dependency = self.cleaned_data.get('dependency')
    office = self.cleaned_data.get('office')

    if Office.objects.filter(dependency=dependency, office__iexact=office).exists():
      self.add_error('office', f"Ya existe la oficina en la dependencia seleccionada")
    cleaned_data = super().clean()
    return cleaned_data