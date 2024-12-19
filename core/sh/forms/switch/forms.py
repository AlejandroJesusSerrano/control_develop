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
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.patchera.models import Patchera

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

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
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

    self._set_initial_data_from_instance()

    self._filter_querysets()

  def _set_initial_data_from_instance(self):

    if not self.instance.pk:
      return

    instance = self.instance

    office = getattr(instance, 'office', None)
    if office and hasattr(office, 'loc') and office.loc and hasattr(office.loc, 'edifice') and office.loc.edifice and hasattr(office.loc.edifice, 'location') and office.dependency and office.dependency.location:

      province = office.loc.edifice.location.province
      dependency = office.dependency
      location = office.loc.edifice.location
      edifice = office.loc.edifice
      loc = office.loc


    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['model'].queryset = Dev_Model.objects.filter(dev_type__dev_type='SWITCH')

    if self.instance.pk:

      if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice and self.instance.office.loc.edifice.location and self.instance.office.loc.edifice.location.province and self.instance.office.dependency and self.instance.office.dependency.location:

        province = self.instance.office.loc.edifice.location.province
        dependency = self.instance.office.dependency
        location = self.instance.office.loc.edifice.location
        edifice = self.instance.office.loc.edifice
        loc = self.instance.office.loc
        office = self.instance.office
        rack = self.instance.rack
        patch_port_in = self.instance.patch_port_in
        patchera = self.instance.patch_port_in.patchera
        switch_port_in = self.instance.switch_port_in
        switch = self.instance.switch_port_in.switch

        self.initial['province'] = province.id
        self.initial['location'] = location.id
        self.initial['dependency'] = dependency.id
        self.initial['edifice'] = edifice.id
        self.initial['loc'] = loc.id
        self.initial['office'] = self.instance.office.id
        self.initial['rack'] = self.instance.rack.id
        self.initial['patchera'] = self.instance.patchera.id

        self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
        self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.office.loc.edifice.location).order_by('edifice')
        self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.office.dependency.location).order_by('dependency')
        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.office.loc.edifice).order_by('office_location')
        self.fields['office'].queryset = Office.objects.filter(loc=self.instance.office.loc, dependency=self.instance.office.dependency).order_by('office')

        if 'province' in self.data:
          try:
            province_id = int(self.data.get('province'))
            self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
            self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
            self.fields['dependency'].queryet = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('office_location')
            self.fields['office'].queryset = Office.objects.filter(
              loc__edifice__location__province_id=province_id,
              dependency__location__province_id=province_id
              ).order_by('office')
            self.fields['rack'].queryset = Rack.objects.filter(
              office__loc__edifice__location__province_id=province_id,
              office__dependency__location__province_id=province_id
              ).order_by('rack')
            self.fields['patchera'].queryset = Patchera.objects.filter(
              rack__office__loc__edifice__location__province_id=province_id,
              rack__office__dependency__location__province_id=province_id
            ).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(
              office__loc__edifice__location__province_id=province_id,
              office__dependency__location__province_id=province_id
            ).order_by('switch')
            if 'rack' in self.data:
              self.fields['switch'].queryset = Switch.objects.filter(
                rack__office__loc__edifice__location__province_id=province_id,
                rack__office__dependency__location__province_id=province_id
              ).order_by('switch')
            elif 'patchera' in self.data:
              self.fields['patchera'].queryset = Switch.objects.filter(
                patchera__rack__office__loc__edifice__location__province_id=province_id,
                patchera__rack__office__dependency__location__province_id=province_id
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
            self.fields['rack'].queryset = Rack.objects.filter(
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
            self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id).order_by('office')
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
            rack_id = int(self.data.get(rack))
            self.fields['patchera'].queryset = Patchera.objects.filter(rack_id=rack_id).order_by('patchera')
            self.fields['switch'].queryset = Switch.objects.filter(
              patchera__rack_id=rack_id,
              rack_id=rack_id).order_by('switch')
          except (ValueError, TypeError):
            pass
        elif self.instace.pk:
          self.fields['patchera'].queryset = self.instance.patchera.rack.patchera_rack.order_by('patchera')

        if 'patchera' in self.data:
          try:
            patchera_id = int(self.data.get(patchera))
            self.fields['switch'].queryset = Switch.objects.filter(patchera_id=patchera_id).order_by('switch')
          except (ValueError, TypeError):
            pass
        elif self.instace.pk:
          self.fields['switch'].queryset = self.instance.switch.patchera.switch_patch_port_in.order_by('switch')

        if office or rack:
          switch_filters = {}
          if office:
            switch_filters['office_id'] = office
          if rack:
            switch_filters['rack_id'] = rack
          self.fields['switch'].queryset = Switch.objects.filter(**switch_filters).distinct()

        if switch:
          pass

  def clean(self):
    cleaned_data = super().clean()
    model = cleaned_data.get('model')
    serial_n = cleaned_data.get('serial_n')
    rack = cleaned_data.get('rack')
    switch_rack_pos = cleaned_data.get('switch_rack_pos')

    if model and serial_n:
      # Excluir el switch actual en caso de edición
      qs = Switch.objects.filter(model=model, serial_n=serial_n)
      if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)

      if qs.exists():
        self.add_error('model', "Ya se encuentra cargado este modelo de Switch")
        self.add_error('serial_n', "El número de serie ya se encuentra registrado y asociado al mismo modelo")

    if rack and switch_rack_pos:
      # Excluir el switch actual en caso de edición
      qs = Switch.objects.filter(rack=rack, switch_rack_pos=switch_rack_pos)
      if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)

      if qs.exists():
        self.add_error('rack', "El switch ya se encuentra en el Rack seleccionado")
        self.add_error('switch_rack_pos', "La posición seleccionada en el Rack, ya se encuentra ocupada")

    return cleaned_data
