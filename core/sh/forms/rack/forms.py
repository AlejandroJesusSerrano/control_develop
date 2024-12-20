from django.forms import *
from django import forms
from django.forms import TextInput, Textarea

from core.sh.models import Rack
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province

class RackForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
    required=False
  )

  location = forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_location'}),
    required=False
  )

  edifice = forms.ModelChoiceField(
    queryset=Edifice.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
    required=False
  )

  loc = forms.ModelChoiceField(
    queryset=Office_Loc.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
    required=False
  )

  dependency = forms.ModelChoiceField(
    queryset=Dependency.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
    required=False
  )
  class Meta:
    model = Rack
    fields = [
      'province', 'location', 'edifice', 'dependency', 'rack', 'office', 'details'
    ]
    widgets = {
      'rack': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el Nombre del Rack',
          'id': 'id_rack_input'
        }
      ),
      'office': Select(
        attrs={
          'class': 'form-control select2',
          'id': 'id_office'
        }
      ),
      'details': Textarea(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese detalles que ayuden a individualizar el Rack',
          'id': 'id_rack_details_input'
        }
      )
    }
    help_texts = {
      'details': '* Aqui puede ingresar referencia de la ubicación, forma, y demas detalles que ayuden a individualizar el Rack'
    }

  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice and self.instance.office.loc.edifice.location and self.instance.office.dependency and self.instance.office.dependency.location:

                province = self.instance.office.loc.edifice.location.province

                self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
                self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.office.loc.edifice.location).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.office.dependency.location).order_by('dependency')
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.office.loc.edifice).order_by('office_location')

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
                self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('office_location')
                self.fields['office'].queryset = Office.objects.filter(loc__edifice__location__province_id=province_id).order_by('office')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['location'].queryset = self.instance.office.loc.edifice.location.province.location_set.order_by('location')

        if 'location' in self.data:
            try:
                location_id = int(self.data.get('location'))
                self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id).order_by('dependency')
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=location_id).order_by('office_location')
                self.fields['office'].queryset = Office.objects.filter(loc__edifice__location_id=location_id).order_by('office')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_location.order_by('edifice')
            self.fields['dependency'].queryset = self.instance.office.dependency.location.dependency_location.order_by('dependency')

        if 'edifice' in self.data:
            try:
                edifice_id = int(self.data.get('edifice'))
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id).order_by('office_location')
                self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=edifice_id).order_by('office')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_edifice.order_by('office_location')

        if 'loc' in self.data:
          try:
            loc_id = int(self.data.get('loc'))
            self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id).order_by('office')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['office'].queryset = self.instance.office.loc.office_location.order_by('office')

  def clean(self):
    rack = self.cleaned_data.get('rack').upper()

    if Rack.objects.filter(rack__iexact=rack).exists():
      self.add_error('rack', f"El Rack que se quiere ingresar, ya existe")
    cleaned_data = super().clean()
    return cleaned_data