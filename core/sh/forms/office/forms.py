from django import forms
from django.forms import TextInput, Textarea
from dal import autocomplete

from core.sh.models import Office
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.province.models import Province

class OfficeForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget = autocomplete.ModelSelect2(
      url = 'dal:province-autocomplete',
      attrs = {
        'class': 'form-control',
        'data-placeholder': 'Seleccione una provincia'
      }
    ),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = autocomplete.ModelSelect2(
      url='dal:location-autocomplete',
      forward=['province'],
      attrs={
        'class': 'form-control',
        'data-placeholder': 'Seleccione una localidad'
        }
      ),
      required=False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = autocomplete.ModelSelect2(
      url='dal:edifice-autocomplete',
      forward=['province', 'location'],
      attrs={
        'class': 'form-control',
        'data-placeholder': 'Seleccione un edificio'
      }
    ),
    required = False
  )

  class Meta:
    model = Office
    fields = [
      'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'description'
      ]
    widgets = {

      'dependency': autocomplete.Select2(
        url='dal:dependency-autocomplete',
        forward=['province', 'location'],
        attrs={
          'class': 'form-control',
          'data-placeholder': 'Seleccione una dependencia'
        }
      ),

      'loc': autocomplete.Select2(
        url='dal:office-loc-autocomplete',
        forward=['province', 'location', 'edifice'],
        attrs={
          'class': 'form-control',
          'data-placeholder': 'Seleccione la locación de la oficina'
          }
        ),

      'office': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre identificatorio para la Oficina'}),
      'description': Textarea(attrs={'class':'form-control', 'placeholder': 'Ingrese una descripción de la oficina'})
    }

    help_texts = {
      'description': '* Esta campo no es obligatorio, pero puede agregar detalles para individualizar la oficina, o agregar algún dato relevenate de la misma.'
    }

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