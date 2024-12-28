from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patchera
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack

class PatcheraForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget = Select(attrs={
      'class': 'form-control select2',
      'id': 'id_province'
    }),
    required=False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = Select(attrs={
      'class': 'form-control select2',
      'id': 'id_location'
    }),
    required=False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = Select(attrs={
      'class': 'form-control select2',
      'id': 'id_edifice'
    }),
    required=False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = Select(attrs={
      'class': 'form-control select2',
      'id': 'id_loc'
    }),
    required=False
  )

  office = forms.ModelChoiceField(
    queryset = Office.objects.all(),
    widget = Select(attrs={
      'class': 'form-control select2',
      'id': 'id_office'
    }),
    required=False
  )


  class Meta:
    model = Patchera
    fields = [
      'province', 'location', 'edifice', 'loc', 'office', 'rack', 'patchera'
    ]
    widgets = {
      'rack': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_rack_patchera'
      }),
      'patchera': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el número de la patchera',
        'id': 'id_patchera_input'
      })
    }
    help_texts = {
      'patchera': '* El número de la patchera, se refiere a la posición de la misma en el Rack'
    }

  def _init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if 'instance' in kwargs and kwargs['instance']:
      instance=kwargs['instance']
      if instance.office and instance.office.loc and instance.office.loc.edifice and instance.office.loc.edifice.location and instance.office.loc.edifice.location.province and instance.office.dependency:
        self.fields['province'].queryset = Province.objects.all()
        self.fields['province'].initial = instance.office.loc.edifice.location.province.id

        self.fields['location'].queryset = Location.objects.filter(province=instance.office.loc.edifice.location.province)
        self.fields['location'].initial = instance.office.loc.edifice.location.id

        self.fields['edifice'].queryset = Edifice.objects.filter(location=instance.office.loc.edifice.location)
        self.fields['edifice'].initial = instance.office.loc.edifice.id

        self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=instance.office.loc.edifice.location)
        self.fields['edifice_ports'].initial = instance.office.loc.edifice.id

        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=instance.office.loc.edifice)
        self.fields['loc'].initial = instance.office.loc.id

        self.fields['office'].queryset = Office.objects.filter(loc=instance.office.loc, dependency=instance.office.dependency)
        self.fields['office'].initial = instance.office.id

  def clean(self):
    rack = self.cleaned_data.get('rack')
    patchera = self.cleaned_data.get('patchera')

    if Patchera.objects.filter(rack=rack, patchera=patchera).exists():
      self.add_error('patchera', f"la posición ingresada en el rack '{rack}', ya se encuentra registrada. Ingrese una diferente")

    cleaned_data = super().clean()
    return cleaned_data