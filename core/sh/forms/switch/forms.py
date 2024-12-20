from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.patchera.models import Patchera
from core.sh.models.switch_port.models import Switch_Port
from core.sh.models.wall_port.models import Wall_Port

class SwitchForm(forms.ModelForm):
  brand = forms.ModelChoiceField(
    queryset = Brand.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_brand'}),
    required = False
  )

  model = forms.ModelChoiceField(
    queryset = Dev_Model.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dev_model'}),
    required = False
  )

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_location'}),
    required = False
  )

  dependency = forms.ModelChoiceField(
    queryset = Dependency.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
    required = False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
    required = False
  )

  edifice_ports = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice_ports'}),
    required = False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
    required = False
  )

  loc_ports = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc_ports'}),
    required = False
  )

  office_ports = forms.ModelChoiceField(
    queryset = Office.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_office_ports'}),
    required = False
  )

  rack_ports = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack_ports'}),
    required = False
  )

  patchera = forms.ModelChoiceField(
    queryset = Patchera.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_patchera'}),
    required = False
  )

  switch = forms.ModelChoiceField(
    queryset = Switch.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch'}),
    required = False
  )

  class Meta:
    model = Switch
    fields = [
      'brand', 'model', 'serial_n', 'ports_q', 'rack', 'switch_rack_pos', 'loc', 'office', 'dependency', 'edifice', 'location', 'wall_port_in', 'switch_port_in', 'patch_port_in'
      ]
    widgets = {
      'serial_n': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el número de serie',
        'id': 'id_serial_n_input'
      }),
      'ports_q': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese la cantidad de puertos del Switch',
        'id': 'id_ports_q_input'
      }),
      'rack': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_rack'
      }),
      'switch_rack_pos': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese la posición del Switch en el Rack',
        'id': 'id_switch_rack_pos_input'
      }),
      'office': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_office'
      }),
      'wall_port_in': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_wall_port_in'
      }),
      'switch_port_in': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_switch_port_in'
      }),
      'patch_port_in': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_patch_port_in'
      })
    }

    help_texts = {
      'ports_q': '* Ingrese solo números',
      'switch_rack_pos': '* Ingrese el número de posición del switch en el rack, en caso de encontrarse en uno'
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if self.instance.pk:

      if self.instance.office and self.instance_office_ports and self.instance.office.loc and self.instance.office_ports.loc_ports and self.instance.office.loc.edifice and self.instance.office_ports.loc_ports.edifice_ports and self.instance.office.loc.edifice.location and self.instance.office_ports.loc_ports.edifice_ports.location and self.instance.dependency and self.instance.dependency.location and ((self.instance.office.rack and self.instance.office.rack.switch and self.instance.office.rack.switch.switch_port_in) or (self.instance.office.switch and self.instance.office.switch.switch_port_in) or (self.instance.office.rack and self.instance.office.rack.patchera and self.instance.office.rack.patchera.patch_port_in)) and self.instance.wall_port_in:

        province = self.instance.office.loc.edifice.location.province

        self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
        self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.office.loc.edifice.location).order_by('edifice')
        self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=self.instance.office_ports.loc_ports.edifice_ports.location).order_by('edifice')
        self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.office.dependency.location).order_by('dependency')
        self.fields['loc'].queryset = Office_Loc.objects.filter(location=self.instance.office.loc.edifice).order_by('office_location')
        self.fields['loc_ports'].queryset = Office_Loc.objects.filter(location=self.instance.office_ports.loc_ports.edifice_ports).order_by('office_location')
        self.fields['office'].queryset = Office.objects.filter(location=self.instance.office.loc).order_by('office')
        self.fields['office_ports'].queryset = Office.objects.filter(location=self.instance.office_ports.loc_ports).order_by('office')
        self.fields['rack'].queryset = Rack.objects.filter(location=self.instance.office.rack.location).order_by('rack')

        self.fields['rack_ports'].queryset = Rack.objects.filter(location=self.instance.office_ports.rack_ports).order_by('rack')

        if self.fields['wall_port_in']:
          self.fields['wall_port_in'].queryset = Wall_Port.filter(location=self.instance.office_ports).order_by('wall_port_in')

        if self.fields['rack']:
          self.fields['rack'].queryset = Rack.objects.filter(location=self.instance.switch_port_in.switch.rack_ports).order_by('rack_ports')

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

        self.fields['brand'].queryset = Brand.objects.all()
        self.fields['model'].queryset = Dev_Model.objects.filter(dev_type__dev_type='SWITCH')

        if 'province' in self.data:
          try:
            province_id = int(self.data.get('province'))
            self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
            self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
            self.fields['edifice_ports'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
            self.fields['dependency'].queryet = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('office_location')
            self.fields['loc_ports'].queryset = Office_Loc.objects.filter(edifice_ports__location__province_id=province_id).order_by('office_location')
            self.fields['office'].queryset = Office.objects.filter(
              loc__edifice__location__province_id=province_id,
              dependency__location__province_id=province_id
            ).order_by('office')
            self.fields['office_ports'].queryset = Office.objects.filter(
              loc_ports__edifice_ports__location__province_id=province_id
            ).order_by('office_ports')
            self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
              office_ports__loc_ports__edifice_ports__location__province_id=province_id
            ).order_by('wall_port_in')
            self.fields['rack'].queryset = Rack.objects.filter(
              office__loc__edifice__location__province_id=province_id,
              office__dependency__location__province_id=province_id
            ).order_by('rack')
            self.fields['rack_ports'].queryset = Rack.objects.filter(
              office_ports__loc_ports__edifice_ports__location__province_id=province_id
            ).order_by('rack_ports')
            self.fields['patchera'].queryset = Patchera.objects.filter(
              rack_ports__office_ports__loc_ports__edifice_ports__location__province_id=province_id,
            ).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(
              office_ports__loc_ports__edifice_ports__location__province_id=province_id,
            ).order_by('switch')
            if 'rack_ports' in self.data:
              self.fields['switch'].queryset = Switch.objects.filter(
                rack_ports__office_ports__loc_ports__edifice_ports__location__province_id=province_id,
              ).order_by('switch')
            elif 'patchera' in self.data:
              self.fields['patchera'].queryset = Switch.objects.filter(
                patchera__rack_ports__office_ports__loc_ports__edifice_ports__location__province_id=province_id,
              ).order_by('switch')
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
            self.fields['office'].queryset = Office.objects.filter(
              loc__edifice__location_id=location_id,
              dependency__location_id=location_id
              ).order_by('office')
            self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
              office__loc__edifice__location_id=location_id
            ).order_by('wall_port_in')
            self.fields['rack'].queryset=Rack.objects.filter(
              office__loc__edifice__location_id=location_id,
              office__dependency__location_id=location_id
              ).order_by('rack')
            self.fields['patchera'].queryset = Patchera.objects.filter(
              rack__office__loc__edifice__location_id=location_id,
              rack__office__dependency__location_id=location_id
            ).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(
              office__loc__edifice__location_id=location_id,
              office__dependency__location_id=location_id
            ).order_by('switch')
            if 'rack' in self.data:
              self.fields['switch'].queryset = Switch.objects.filter(
                rack__office__loc__edifice__location_id=location_id,
                rack__office__dependency__location_id=location_id
              ).order_by('switch')
            elif 'patchera' in self.data:
              self.fields['patchera'].queryset = Switch.objects.filter(
                patchera__rack__office__loc__edifice__location_id=location_id,
                patchera__rack__office__dependency__location_id=location_id
              ).order_by('switch')
          except (ValueError, TypeError):
                pass
        elif self.instance.pk:
          self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_location.order_by('edifice')
          self.fields['dependency'].queryset = self.instance.office.dependency.location.dependency_location.order_by('dependency')

        if 'dependency' in self.data:
          try:
            dependency_id = int(self.data.get('dependency'))
            self.fields['office'].queryset = Office.objects.filter(
              dependency_id=dependency_id
            ).order_by('office')
            self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
              office__dependency__location_id=location_id
            ).order_by('wall_port_in')
            self.fields['rack'].queryset = Rack.objects.filter(
              office__dependency__location_id=location_id
            ).order_by('rack')
            self.fields['patchera'].queryset = Patchera.objects.filter(
              rack__office__dependency__location_id=location_id
            ).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(
              office__dependency__location_id=location_id
            ).order_by('switch')
            if 'rack' in self.data:
              self.fields['switch'].queryset = Switch.objects.filter(
                rack__office__dependency__location_id=location_id
              ).order_by('switch')
            elif 'patchera' in self.data:
              self.fields['patchera'].queryset = Switch.objects.filter(
                patchera__rack__office__dependency__location_id=location_id
              ).order_by('switch')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['office'].queryset = self.instance.office.dependency.offices_dependencies.order_by('office')

        if 'edifice' in self.data:
          try:
            edifice_id = int(self.data.get('edifice'))
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice_id).order_by('office_location')
            self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=edifice_id).order_by('office')
            self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office__loc__edifice_id=edifice_id).order_by('wall_port_in')
            self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice_id=edifice_id).order_by('rack')
            self.fields['patchera'].queryset = Patchera.objects.filter(rack__loc__edifice_id=edifice_id).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(office__loc__edifice_id=edifice_id).order_by('switch')
            if 'rack' in self.data:
              self.fields['switch'].queryset = Switch.objects.filter(rack__office__loc__edifice_id=edifice_id).order_by('switch')
            elif 'patchera' in self.data:
              self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office__loc__edifice_id=edifice_id).order_by('switch')

          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_edifice.order_by('office_location')

        if 'loc' in self.data:
          try:
            loc_id = int(self.data.get('loc'))
            self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id).order_by('office')
            self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office__loc_id=loc_id).order_by('wall_port_in')
            self.fields['rack'].queryset = Rack.objects.filter(office__loc_id=loc_id).order_by('rack')
            self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__loc_id=loc_id).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(office__loc_id=loc_id).order_by('switch')
            if 'rack' in self.data:
              self.fields['switch'].queryset = Switch.objects.filter(rack__office__loc_id=loc_id).order_by('switch')
            elif 'patchera' in self.data:
              self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office__loc_id=loc_id).order_by('switch')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['office'].queryset = self.instance.office.loc.office_location.order_by('office')

        if 'office' in self.data:
          try:
            office_id = int(self.data.get('office'))
            self.fields['wall_port_in'].queryset = Wall_Port.objects.filter('office_id=office_id').order_by('wall_port_in')
            self.fields['rack'].queryset = Rack.objects.filter(office_id=office_id).order_by('rack')
            self.fields['patchera'].queryset = Patchera.objects.filter(rack__office_id=office_id).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(office_id=office_id).order_by('switch')
            if 'rack' in self.data:
                self.fields['switch'].queryset = Switch.objects.filter(rack__office_id=office_id).order_by('switch')
            elif 'patchera' in self.data:
                self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office_id=office_id).order_by('switch')
          except (ValueError, TypeError):
            pass
        elif self.instance.pk:
          self.fields['rack'].queryset = self.instance.rack.office.rack_office.order_by('rack')

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
    model = cleaned_data.get('model')
    serial_n = cleaned_data.get('serial_n')
    rack = cleaned_data.get('rack')
    switch_rack_pos = cleaned_data.get('switch_rack_pos')

    if Switch.objects.filter(model=model, serial_n=serial_n).exists():
      self.add_error('model', f'Ya se encuentra registrado el switch {model} con el S/N° {serial_n}.')
      self.add_error('serial_n', f'El S/N° {serial_n}, ya se ecuentra registrado para el switch {model}.')

    if Switch.objects.filter(rack=rack, switch_rack_pos=switch_rack_pos).exists():
      self.add_error('rack', f'ya se encuentra ocupáda la posicion {switch_rack_pos} en el rack {rack}')
      self.add_error('switch_rack_pos', f'el rack {rack}, ya tiene ocupada la posicion de switch {switch_rack_pos}')
    return cleaned_data
