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

    if 'province' in self.data:
      try:
        province_id = int(self.data.get('province'))

        self.fields['location'].queryset = Location.objects.filter(
          province_id=province_id
        ).order_by('location')

        self.fields['edifice'].queryset = Edifice.objects.filter(
          location__province_id=province_id
        ).order_by('edifice')

        self.fields['loc'].queryset = Office_Loc.objects.filter(
          edifice__location__province_id=province_id
        ).order_by('office_location')

        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice__location__province_id=province_id,
          dependency__location__province_id=province_id
        ).order_by('office')

        self.fields['rack'].queryset = Rack.objects.filter(
          office__loc__edifice__location__province_id=province_id,
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'location' in self.data:
      try:
        location_id = int(self.data.get('location'))
        self.fields['edifice'].queryset = Edifice.objects.filter(
          location_id=location_id
        ).order_by('edifice')

        self.fields['loc'].queryset = Office_Loc.objects.filter(
          edifice__location_id=location_id
        ).order_by('office_location')

        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice__location_id=location_id,
          dependency__location_id=location_id
        ).order_by('office')

        self.fields['rack'].queryset = Rack.objects.filter(
          office__loc__edifice__location_id=location_id,
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'edifice' in self.data:
      try:
        edifice_id = int(self.data.get('edifice'))
        self.fields['loc'].queryset = Office_Loc.objects.filter(
          edifice_id=edifice_id
        ).order_by('office_location')

        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice_id=edifice_id,
          dependency__edifice_id=edifice_id
        ).order_by('office')

        self.fields['rack'].queryset = Rack.objects.filter(
          office__loc__edifice_id=edifice_id,
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'loc' in self.data:
      try:
        loc_id = int(self.data.get('loc'))
        self.fields['office'].queryset = Office.objects.filter(
          loc_id=loc_id,
          dependency_id=loc_id
        ).order_by('office')

        self.fields['rack'].queryset = Rack.objects.filter(
          office__loc_id=loc_id,
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'office' in self.data:
      try:
        office_id = int(self.data.get('office'))
        self.fields['rack'].queryset = Rack.objects.filter(
          office_id=office_id,
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

  def clean(self):
    rack = self.cleaned_data.get('rack')
    patchera = self.cleaned_data.get('patchera')

    if Patchera.objects.filter(rack=rack, patchera=patchera).exists():
      self.add_error('patchera', f"la posición ingresada en el rack '{rack}', ya se encuentra registrada. Ingrese una diferente")

    cleaned_data = super().clean()
    return cleaned_data