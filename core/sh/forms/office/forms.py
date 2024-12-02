from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Office
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.province.models import Province

class OfficeForm(forms.ModelForm):

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

  edifice = forms.ModelChoiceField(
    queryset=Edifice.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Office
    fields = [
      'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'description'
      ]
    widgets = {

      'dependency': Select(attrs={'class': 'form-control', 'data-placeholder': 'Seleccione una dependencia'}),
      'loc': Select(attrs={'class': 'form-control', 'data-placeholder': 'Seleccione la locación de la oficina'}),
      'office': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre identificatorio para la Oficina'}),
      'description': Textarea(attrs={'class':'form-control', 'placeholder': 'Ingrese una descripción de la oficina'})
    }

    help_texts = {
      'description': '* Esta campo no es obligatorio, pero puede agregar detalles para individualizar la oficina, o agregar algún dato relevenate de la misma.'
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # Filtrado dinámico: inicializar valores vacíos en cascada
    self.fields['location'].queryset = Location.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()
    self.fields['dependency'].queryset = Dependency.objects.none()

        # Cargar datos si hay valores previos (en caso de edición)
    if 'province' in self.data:
        try:
            province_id = int(self.data.get('province'))
            self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('name')
        except (ValueError, TypeError):
            pass  # Provincia no seleccionada, mantener queryset vacío
    elif self.instance.pk:
        self.fields['location'].queryset = self.instance.location.province.location_set.order_by('name')

    if 'location' in self.data:
        try:
            location_id = int(self.data.get('location'))
            self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('name')
        except (ValueError, TypeError):
            pass  # Localidad no seleccionada, mantener queryset vacío
    elif self.instance.pk:
        self.fields['edifice'].queryset = self.instance.edifice.location.edifice_set.order_by('name')

    if 'edifice' in self.data:
        try:
            edifice_id = int(self.data.get('edifice'))
            self.fields['dependency'].queryset = Dependency.objects.filter(edifice_id=edifice_id).order_by('name')
        except (ValueError, TypeError):
            pass  # Edificio no seleccionado, mantener queryset vacío
    elif self.instance.pk:
        self.fields['dependency'].queryset = self.instance.edifice.dependency_set.order_by('name')

  def clean(self):
    cleaned_data = super().clean()
    dependency = self.cleaned_data.get('dependency')
    office = self.cleaned_data.get('office')

    if office and dependency:
      office = office.strip()
      qs = Office.objects.filter(dependency=dependency, office__iexact=office)
      if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)
      if qs.exists():
        self.add_error('office', f"Ya existe la oficina en la dependencia seleccionada")

    return cleaned_data