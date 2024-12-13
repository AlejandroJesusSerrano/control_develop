from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Wall_Port
from core.sh.models.dependency.models import Dependency
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
    queryset = Office.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  rack = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  patchera = forms.ModelChoiceField(
    queryset = Patchera.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required  = False
  )

  switch = forms.ModelChoiceField(
    queryset = Switch.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )


  class Meta:
    model = Wall_Port
    fields = 'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in', 'details', 'wall_port'
    widgets = {
      'office': Select(attrs={'class': 'form-control select2', 'placeholder': 'Seleccione la Oficina'}),
      'wall_port': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el puerto/boca de la pared'}),
      'switch_port_in': Select(attrs={'class': 'form-control select2', 'placeholder': 'Seleccione el puerto del switch de origen'}),
      'patch_port_in': Select(attrs={'class': 'form-control select2', 'placeholder': 'Seleccione el puerto de la patchera de origen'}),
      'details': Textarea(attrs={'class': 'form-control', 'placeholder': 'De ser necesario, ingrese detalles particulares'}),
    }

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

      if self.instance.pk:
        if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice and self.instance.office.loc.edifice.location and self.instance.dependency and self.instance.dependency.location and ((self.instance.office.rack and self.instance.office.rack.switch and self.instance.office.rack.switch.switch_port_in) or (self.instance.office.switch and self.instance.office.switch.switch_port_in) or (self.instance.office.rack and self.instance.office.rack.patchera and self.instance.office.rack.patchera.patch_port_in)):

          province = self.instance.office.loc.edifice.location.province

          self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
          self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.office.loc.edifice.location).order_by('edifice')
          self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.office.dependency.location).order_by('dependency')
          self.fields['loc'].queryset = Office_Loc.objects.filter(location=self.instance.office.loc.edifice).order_by('office_location')
          self.fields['office'].queryset = Office.objects.filter(location=self.instance.office.loc).order_by('office')

          if self.fields['rack']:
            self.fields['rack'].queryset = Rack.objects.filter(location=self.instance.office).order_by('rack')
            if self.fields['switch']:
              self.fields['switch'].queryset = Switch.objects.filter(location=self.instance.office.rack).order_by('switch')
              self.fields['switch_port_in'].queryset = Switch_Port(location=self.instance.office.rack.switch).order_by('switch_port_in')
            elif self.fields['patchera']:
              self.fields['patchera'].queryset = Patchera(location=self.instance.office.rack).order_by('patchera')
              self.fields['patch_port_in'].queryset = Patch_Port(location=self.instance.office.rack.patchera).order_by('patch_port_in')
          elif self.fields['switch']:
            self.fields['switch'].queryset = Switch.objects.filter(location=self.instance.office).order_by('switch')
            self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(location=self.instance.office.switch).order_by('switch_port_in')
          else: None

          if province in self.data:
            try:
              province_id = int(self.get('province'))
              self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
              self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
              self.fields['dependency'].queryset = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
              self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('loc')
              self.fields['office'].queryset = Office.objects.filter(loc__edifice__location__province_id=province_id).order_by('office')
              self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice__location__province_id=province_id).order_by('rack')

              self.fields['switch'].queryset = Switch.objects.filter(
                    office__loc__edifice__location__province_id=province_id,
                    rack__office__loc__edifice__location__province_id=province_id
                    ).order_by('switch')

              self.fields['patchera'] = Patchera.objects.filter(
                  rack__office__loc__edifice__location__province_id=province_id).order_by('patchera')

              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
                    switch__office__loc__edifice__location__province_id=province_id,
                    switch__rack__office__loc__edifice__location__province_id=province_id
                    ).order_by('port_id')

              self.fields['patch_port_in'] = Patch_Port.objects.filter(patchera__rack__office__loc__edifice__location__province_id=province_id).order_by('patch_port')
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
              self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice__location_id=location_id).order_by('rack')

              self.fields['switch'].queryset = Switch.objects.filter(
                office__loc__edifice__location_id=location_id,
                rack__office__loc__edifice__location_id=location_id
              ).order_by('switch')

              self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__loc__edifice__location_id=location_id).order_by('patchera')

              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
                switch__rack__office__loc__edifice__location_id=location_id,
                switch__office__loc__edifice__location_id=location_id
              ).order_by('switch_port')

              self.fields['patch_port_in'] = Patch_Port.objects.filter(patchera__rack__office__loc__edifice__location_id=location_id).order_by('patch_port')
            except (ValueError, TypeError):
              pass
          elif self.instance.pk:
            self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_location.order_by('edifice')
            self.fields['edifice'].queryset = self.instance.office.dependency.location.dependency_location.order_by('dependency')

          if 'dependency' in self.data:
            try:
              dependency_id=int(self.data.get('dependency'))
              self.fields['loc'].queryset = Office_Loc.objects.filter(dependency_id=dependency_id).order_by('office_location')
              self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id).order_by('office')
              self.fields['rack'].queryset = Rack.objects.filter(office__dependency_id=dependency_id).order_by('rack')

              self.fields['switch'].queryser = Switch.objects.filter(
                rack__office__dependency_id=dependency_id,
                office__dependency_id=dependency_id
              ).order_by('switch')

              self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__dependency_id=dependency_id).order_by('patchera')

              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
                switch__rack__office__dependency_id=dependency_id,
                switch__office__dependency_id=dependency_id
              ).order_by('switch_port_in')

              self.fields['patch_port_in'] = Patch_Port.objects.filter(patchera__rack__office__dependency_id=dependency_id).order_by('patch_port_in')
            except(ValueError, TypeError):
              pass
          elif self.instance.pk:
            self.fields['office'].queryset = self.instance.office.dependency.offices_dependencies.order_by('office_location')

          if 'edifice' in self.data:
            try:
              edifice_id=int(self.data.get('edifice'))
              self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id).order_by('office_location')
              self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=edifice_id).order_by('office')
              self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice_id=edifice_id).order_by('rack')

              self.fields['switch'].queryser = Switch.objects.filter(
                rack__office__loc__edifice_id=edifice_id,
                office__loc__edifice_id=edifice_id
              ).order_by('switch')

              self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__loc__edifice_id=edifice_id).order_by('patchera')

              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
                switch__rack__office__loc__edifice_id=edifice_id,
                switch__office__loc__edifice_id=edifice_id
              ).order_by('switch_port_in')

              self.fields['patch_port_in'] = Patch_Port.objects.filter(patchera__rack__office__loc__edifice_id=edifice_id).order_by('patch_port_in')
            except(ValueError, TypeError):
              pass
          elif self.instance.pk:
            self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_edifice.order_by('office_location')

          if 'loc' in self.data:
            try:
              loc_id = int(self.data.get('loc'))
              self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id).order_by('office')
              self.fields['rack'].queryset = Rack.objects.filter(office__loc_id=loc_id).order_by('rack')

              self.fields['switch'].queryset = Switch.objects.filter(
                rack__office__loc_id=loc_id,
                office__loc_id=loc_id
              ).order_by('switch')

              self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__loc_id=loc_id).order_by('patchera')

              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
                switch__rack__office__loc_id=loc_id,
                switch__office__loc_id=loc_id
              ).order_by('switch_port_in')

              self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera__rack__office__loc_id=loc_id).order_by('patch_port')
            except(ValueError, TypeError):
              pass
          elif self.instance.pk:
            self.fields['office'].queryset = self.instance.office.loc.office_location.order_by('office')

          if 'office' in self.data:
            try:
              office_id=int(self.data.get('office'))
              self.fields['rack'].queryset = Rack.objects.filter(office_id=office_id).order_by('rack')

              self.fields['switch'].queryset = Switch.objects.filter(
                rack__office_id=office_id,
                office_id=office_id
              )

              self.fields['patchera'].queryset = Patchera.objects.filter(rack__office_id=office_id).order_by('patchera')

              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
                switch__rack__office_id=office_id,
                switch__office_id=office_id
              ).order_by('switch_port_in')

              self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera__rack__office_id=office_id).order_by('patch_port_in')
            except(ValueError, TypeError):
              pass
          elif self.instance.pk:
            self.fields['rack'].queryset = self.instance.office.rack.rack_office.order_by('rack')
            self.fields['switch'].queryset = self.instance.office.switch.switch_office.order_by('switch')

          if 'rack' in self.data:
            try:
              rack_id=int(self.data.get('rack'))
              self.fields['switch'].queryset = Switch.objects.filter(rack_id=rack_id).order_by('switch')
              self.fields['patchera'].queryset = Patchera.objects.filter(rack_id=rack_id).order_by('patchera')
              self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__rack_id=rack_id).order_by('switch_port')
              self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera__rack_id=rack_id).order_by('patch_port_in')
            except (ValueError, TypeError):
              pass
          elif self.instance.pk:
            self.fields['switch'].queryset = self.instance.office.rack.switch.switch_rack.order_by('switch')
            self.fields['patchera'].queryset = self.instance.office.patchera.patchera_rack.order_by('patchera')

          if 'switch' in self.data:
            try:
              switch_id=int(self.data.get('switch'))
              self.fields['switch_por_in'].queryset = Switch_Port.objects.filter(switch_id=switch_id).order_by('switch_port_in')
            except (ValueError, TypeError):
              pass

          if 'patchera' in self.data:
            try:
              patchera_id=int(self.data.get('patchera'))
              self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera_id=patchera_id).order_by('patch_port_in')
            except (ValueError, TypeError):
              pass

    def clean(self):
      cleaned_data = super().clean()
      office = cleaned_data.get('office')
      wall_port = cleaned_data.get('wall_port')
      # Verifica el constraint de unicidad
      if Wall_Port.objects.filter(office=office, wall_port=wall_port).exists():
        self.add_error('wall_port', 'Esta boca de pared ya existe en la oficina seleccionada.')
      return cleaned_data