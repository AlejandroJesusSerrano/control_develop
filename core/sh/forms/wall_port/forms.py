from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Wall_Port
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.switch_port.models import Switch_Port

class WallPortForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  dependency = forms.ModelChoiceField(
    queryset = Dependency.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  office = forms.ModelChoiceField(
    queryset = Dev_Model.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  rack = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  patchera_in = forms.ModelChoiceField(
    queryset = Patchera.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required  = False
  )

  switch_in = forms.ModelChoiceField(
    queryset = Switch.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )


  class Meta:
    model = Wall_Port
    fields = 'province', 'location', 'dependency', 'edifice', 'loc', 'office', 'rack', 'switch_in', 'patchera_in'
    widgets = {
      'office': Select(attrs={'class': 'form-control select2', 'placeholder': 'Seleccione la Oficina'}),
      'wall_port': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el puerto/boca de la pared'}),
      'switch_port_in': Select(attrs={'class': 'form-control select2', 'placeholder': 'Seleccione el puerto del switch de origen'}),
      'patch_port_in': Select(attrs={'class': 'form-control select2', 'placeholder': 'Seleccione el puerto de la patchera de origen'}),
      'details': Textarea(attrs={'class': 'form-control', 'placeholder': 'De ser necesario, ingrese detalles particulares'}),
    }

    def __init__(self, *args, **kwargs):
      super(WallPortForm, self).__init__(*args, **kwargs)
      self.fields['province'].queryset = Province.objects.all()
      self.fields['location'].queryset = Location.objects.all()
      self.fields['dependency'].queryset = Dependency.objects.all()
      self.fields['edifice'].queryset = Edifice.objects.all()
      self.fields['loc'].queryset = Office_Loc.objects.all()
      self.fields['office'].queryset = Office.objects.all()
      self.fields['rack'].queryset = Rack.objects.all()
      self.fields['switch_port_in'].queryset = Switch_Port.objects.all()
      self.fields['patch_port_in'].queryset = Patch_Port.objects.all()

      if self.instance.pk:
        self.initial['province'] = self.office.loc.edfice.location.province
        self.initial['location'] = self.office.loc.edifice.location
        self.initial['dependency'] = self.office.dependency
        self.initial['edifice']= self.office.loc.edifice
        self.initial['loc'] = self.office.loc
        self.initial['office']= self.office
        if self.switch_port_in:
          self.initial['rack']= self.switch_port_in.switch.rack
        elif self.patch_port_in:
          self.initial['rack']= self.patch_port_in.patchera.rack
        else:
          'No llega a Rack'
        self.initial['patch_port_in'] = self.patch_port_in
        self.initial['switch_port_in'] = self.switch_port_in

      else:
        selected_province = self.data.get('province')
        selected_location = self.data.get('location')
        selected_dependency = self.data.get('dependency')
        selected_edifice = self.data.get('edifice')
        selected_loc = self.data.get('loc')
        selected_office = self.data.get('office')
        selected_rack = self.data.get('rack')
        selected_patchera_in = self.data.get('patchera_in')
        selected_patchera_out = self.data.get('patchera_out')
        selected_switch_in = self.data.get('switch_in')
        selected_switch_out = self.data.get('switch_out')

      def to_int(value):
        try:
          return int(value)
        except (ValueError, TypeError):
          return None

      selected_province = to_int(selected_province)
      selected_location = to_int(selected_location)
      selected_dependency = to_int(selected_dependency)
      selected_edifice = to_int(selected_edifice)
      selected_loc = to_int(selected_loc)
      selected_office = to_int(selected_office)
      selected_rack = to_int(selected_rack)
      selected_patchera_in = to_int(selected_patchera_in)
      selected_patchera_out = to_int(selected_patchera_out)
      selected_switch_in = to_int(selected_switch_in)
      selected_switch_out = to_int(selected_switch_out)

      if selected_province:
        self.fields['location'].queryset = Location.objects.filter(province_id=selected_province)
        self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=selected_province)
        self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location__province_id=selected_province).distinct()
        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=selected_province)
        self.fields['office'].queryset = Office.objects.filter(loc__edifice__location__province_id=selected_province)

      if selected_location:
        self.fields['edifice'].queryset = Edifice.objects.filter(location_id=selected_location)
        self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location_id=selected_location).distinct()
        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=selected_location)
        self.fields['office'].queryset = Office.objects.filter(loc__edifice__location_id=selected_location)

      if selected_edifice:
        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=selected_edifice)
        self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=selected_edifice)

      if selected_loc:
        self.fields['office'].queryset = Office.objects.filter(loc_id=selected_loc)

      if selected_dependency:
        self.fields['office'].queryset = self.fields['office'].queryset.filter(dependency_id=selected_dependency).distinct()

      if selected_rack:
        self.fields['patchera_in'].queryset = Patchera.objects.filter(rack_id=selected_rack)
        self.fields['patchera_out'].queryset = Patchera.objects.filter(rack_id=selected_rack)
        self.fields['switch_in'].queryset = Switch.objects.filter(rack_id=selected_rack)
        self.fields['switch_out'].queryset = Switch.objects.filter(rack_id=selected_rack)

    def clean(self):
      cleaned_data = super().clean()
      office = cleaned_data.get('office')
      wall_port = cleaned_data.get('wall_port')

      # Verifica el constraint de unicidad
      if Wall_Port.objects.filter(office=office, wall_port=wall_port).exists():
        self.add_error('wall_port', 'Esta boca de pared ya existe en la oficina seleccionada.')
      return cleaned_data