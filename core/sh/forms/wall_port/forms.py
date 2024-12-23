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
    widget = forms.Select(attrs = {'class': 'form-control', 'id': 'id_province'}),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_location'}),
    required = False
  )

  dependency = forms.ModelChoiceField(
    queryset = Dependency.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_dependency'}),
    required = False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_edifice'}),
    required = False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_loc'}),
    required = False
  )

  edifice_port = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_edifice_port'}),
    required = False
  )

  loc_port = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_loc_port'}),
    required = False
  )

  office_port = forms.ModelChoiceField(
    queryset = Office.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_office_port'}),
    required = False
  )

  rack_port = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_rack_port'}),
    required = False
  )

  patchera = forms.ModelChoiceField(
    queryset = Patchera.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_patchera'}),
    required  = False
  )

  switch = forms.ModelChoiceField(
    queryset = Switch.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2', 'id': 'id_switch'}),
    required = False
  )


  class Meta:
    model = Wall_Port
    fields = [
      'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'edifice_port', 'loc_port', 'office_port', 'rack_port', 'switch', 'switch_port_in', 'patchera', 'patch_port_in', 'details', 'wall_port'
      ]

    widgets = {
      'office': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_office'
      }),
      'wall_port': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el puerto/boca de la pared',
        'id': 'id_wall_port_input'
      }),
      'switch_port_in': Select(attrs={
        'class': 'form-control select2',
        'id':'id_switch_port_in'
      }),
      'patch_port_in': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_patch_port_in'
      }),
      'details': Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'De ser necesario, ingrese detalles particulares',
        'id': 'id_details_input'
      }),
    }

  def __init__(self, *args, **kwargs):
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

        self.fields['dependency'].queryset = Dependency.objects.filter(
          location__province_id=province_id
        ).order_by('dependency')

        self.fields['loc'].queryset = Office_Loc.objects.filter(
          edifice__location__province_id=province_id
        ).order_by('office_location')

        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice__location__province_id=province_id
        ).order_by('office')

        self.fields['edifice_port'].queryset = Edifice.objects.filter(
          location__province_id=province_id
        ).order_by('edifice')

        self.fields['loc_port'].queryset = Office_Loc.objects.filter(
          edifice__location__province_id=province_id
        ).order_by('office_location')

        self.fields['office_port'].queryset = Office.objects.filter(
          loc__edifice__location__province_id=province_id
        ).order_by('office')

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office__loc__edifice__location__province_id=province_id
        ).order_by('rack')

        self.fields['switch'].queryset = Switch.objects.filter(
          office__loc__edifice__location__province_id=province_id,
          rack__office__loc__edifice__location__province_id=province_id
        ).order_by('switch')

        self.fields['patchera'].queryset = Patchera.objects.filter(
          rack__office__loc__edifice__location__province_id=province_id
        ).order_by('patchera')

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__office__loc__edifice__location__province_id=province_id,
          switch__rack__office__loc__edifice__location__province_id=province_id
        ).order_by('switch_port_in')

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack__office__loc__edifice__location__province_id=province_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if 'location' in self.data:
      try:
        location_id = int(self.data.get('location'))

        self.fields['edifice'].queryset = Edifice.objects.filter(
          location_id=location_id
        ).order_by('edifice')

        self.fields['dependency'].queryset = Dependency.objects.filter(
          location_id=location_id
        ).order_by('dependency')

        self.fields['loc'].queryset = Office_Loc.objects.filter(
          edifice__location_id=location_id
        ).order_by('office_location')

        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice__location_id=location_id
        ).order_by('office')

        self.fields['edifice_port'].queryset = Edifice.objects.filter(
          location_id=location_id
        ).order_by('edifice')

        self.fields['loc_port'].queryset = Office_Loc.objects.filter(
          edifice__location_id=location_id
        ).order_by('office_location')

        self.fields['office_port'].queryset = Office.objects.filter(
          loc__edifice__location_id=location_id
        ).order_by('office')

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office__loc__edifice__location_id=location_id
        ).order_by('rack')

        self.fields['switch'].queryset = Switch.objects.filter(
          office__loc__edifice__location_id=location_id,
          rack__office__loc__edifice__location_id=location_id
        ).order_by('switch')

        self.fields['patchera'].queryset = Patchera.objects.filter(
          rack__office__loc__edifice__location_id=location_id
        ).order_by('patchera')

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__office__loc__edifice__location_id=location_id,
          switch__rack__office__loc__edifice__location_id=location_id
        ).order_by('switch_port_in')

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack__office__loc__edifice__location_id=location_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if 'dependency' in self.data:
      try:
        dependency_id = int(self.data.get('dependency'))

        self.fields['office'].queryset = Office.objects.filter(
          dependency_id=dependency_id
        ).order_by('office')

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office__dependency_id=dependency_id
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
          loc__edifice_id=edifice_id
        ).order_by('office')

      except (ValueError, TypeError):
        pass

    if 'loc' in self.data:
      try:
        loc_id = int(self.data.get('loc'))

        self.fields['office'].queryset = Office.objects.filter(
          loc_id=loc_id
        ).order_by('office')

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office__loc_id=loc_id
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'office' in self.data:
      try:
        office_id = int(self.data.get('office'))

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office_id=office_id
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'edifice_port' in self.data:
      try:
        edifice_port_id = int(self.data.get('edifice_port'))

        self.fields['loc_port'].queryset = Office_Loc.objects.filter(
          edifice_id=edifice_port_id
        ).order_by('office_location')

        self.fields['office_port'].queryset = Office.objects.filter(
          loc__edifice_id=edifice_port_id
        ).order_by('office')

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office__loc__edifice_id=edifice_port_id
        ).order_by('rack')

        self.fields['switch'].queryset = Switch.objects.filter(
          office__loc__edifice_id=edifice_port_id,
          rack__office__loc__edifice_id=edifice_port_id
        ).order_by('switch')

        self.fields['patchera'].queryset = Patchera.objects.filter(
          rack__office__loc__edifice_id=edifice_port_id
        ).order_by('patchera')

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__office__loc__edifice_id=edifice_port_id,
          switch__rack__office__loc__edifice_id=edifice_port_id
        ).order_by('switch_port_in')

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack__office__loc__edifice_id=edifice_port_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if 'loc_port' in self.data:
      try:
        loc_port_id = int(self.data.get('loc_port'))

        self.fields['office_port'].queryset = Office.objects.filter(
          loc_id=loc_port_id
        ).order_by('office')

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office__loc_id=loc_port_id
        ).order_by('rack')

        self.fields['switch'].queryset = Switch.objects.filter(
          office__loc_id=loc_port_id,
          rack__office__loc_id=loc_port_id
        ).order_by('switch')

        self.fields['patchera'].queryset = Patchera.objects.filter(
          rack__office__loc_id=loc_port_id
        ).order_by('patchera')

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__office__loc_id=loc_port_id,
          switch__rack__office__loc_id=loc_port_id
        ).order_by('switch_port_in')

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack__office__loc_id=loc_port_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if 'office_port' in self.data:
      try:
        office_port_id = int(self.data.get('office_port'))

        self.fields['rack_port'].queryset = Rack.objects.filter(
          office_id=office_port_id
        ).order_by('rack')

        self.fields['switch'].queryset = Switch.objects.filter(
          rack__office_id=office_port_id,
          office_id=office_port_id
        ).order_by('switch')

        self.fields['patchera'].queryset = Patchera.objects.filter(
          rack__office_id=office_port_id
        ).order_by('patchera')

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__rack__office_id=office_port_id,
          switch__office_id=office_port_id
        ).order_by('switch_port_in')

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack__office_id=office_port_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if 'rack_port' in self.data:
      try:
        rack_port_id = int(self.data.get('rack_port'))

        self.fields['switch'].queryset = Switch.objects.filter(
          rack_id=rack_port_id
        ).order_by('switch')

        self.fields['patchera'].queryset = Patchera.objects.filter(
          rack_id=rack_port_id
        ).order_by('patchera')

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__rack_id=rack_port_id
        ).order_by('switch_port_in')

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack_id=rack_port_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if 'switch' in self.data:
      try:
        switch_id = int(self.data.get('switch'))

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch_id=switch_id
        ).order_by('switch_port_in')
      except (ValueError, TypeError):
        pass

    if 'patchera' in self.data:
      try:
        patchera_id = int(self.data.get('patchera'))

        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera_id=patchera_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    if self.instance.pk:
      if self.instance.office and self.instance.office.loc:
        self.fields['location'].queryset = self.instance.office.loc.edifice.location.province.location_set.order_by('location')
        self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_location.order_by('edifice')
        self.fields['dependency'].queryset = self.instance.office.dependency.location.dependency_location.order_by('dependency')
        self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_edifice.order_by('office_location')
        self.fields['office'].queryset = Office.objects.filter(
          loc=self.instance.office.loc
        ).order_by('office')
        self.fields['rack_port'].queryset = Rack.objects.filter(
          office=self.instance.office
        ).order_by('rack')

      if hasattr(self.instance, 'office_port'):
        self.fields['rack_port'].queryet = Rack.objects.filter(
          office=self.instance.office_port
        ).order_by('rack')

      if hasattr(self.instance.office.loc, 'edifice'):
        edifice = self.instance.office.loc.edifice
        self.fields['edifice_port'].queryset = Edifice.objects.filter(
          location=edifice.location
        ).order_by('edifice')
        self.fields['loc_port'].queryset = Office_Loc.objects.filter(
          edifice=edifice
        ).order_by('office_location')

        if self.instance.office:
          self.fields['office_port'].queryset = Office.objects.filter(
            loc__edifice=edifice
          ).order_by('office')

      if self.instance.switch_port_in and hasattr(self.instance.switch_port_in, 'switch'):
        switch = self.instance.switch_port_in.switch

        self.fields['switch'].queryset = Switch.objects.filter(
          id=switch.id
        )
        self.initial['switch'] = switch.id

        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch=switch
        ).order_by('port_id')
        self.initial['switch_port_in'] = self.instance.switch_port_in.id

      if self.instance.patch_port_in:
        patchera = self.instance.patch_port_in.patchera
        if patchera:
          self.fields['patchera'].queryset = Patchera.objects.filter(
            rack=patchera.rack,
          ).order_by('patchera')

          self.initial['patchera'] = patchera.id

          self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
            patchera=patchera
          ).order_by('patch_port_in')

          self.initial['patch_port_in'] = self.instance.patch_port_in.id

  def clean(self):
    cleaned_data = super().clean()
    office = cleaned_data.get('office')
    wall_port = cleaned_data.get('wall_port')

    if Wall_Port.objects.filter(office=office, wall_port=wall_port).exists():
      self.add_error('wall_port', 'Esta boca de pared ya existe en la oficina seleccionada.')
    return cleaned_data