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

        if 'province' in self.fields and province:
          self.initial['province'] = province.id
        if 'location' in self.fields and location:
          self.initial['location'] = location.id
        if 'dependency' in self.fields and dependency:
          self.initial['dependency'] = dependency.id
        if 'edifice' in self.fields and edifice:
          self.initial['edifice'] = edifice.id
        if 'loc' in self.fields and loc:
          self.initial['loc'] = loc.id
        if 'office' in self.fields and office:
          self.initial['office'] = office.id

        rack = getattr(instance, 'rack', None)
        patch_port_in = getattr(instance, 'patch_port_in', None)
        switch_port_in = getattr(instance, 'switch_port_in', None)
        patchera = patch_port_in.patchera if patch_port_in else None
        switch_obj = switch_port_in.switch if switch_port_in else None

        if 'rack' in self.fields and rack:
          self.initial['rack'] = rack.id
        if 'patchera' in self.fields and patchera:
          self.initial['patchera'] = patchera.id
        if 'switch' in self.fields and switch_obj:
          self.initial['switch'] = switch_obj.id

        patch_port_in = getattr(instance, 'patch_port_in', None)
        switch_port_in = getattr(instance, 'switch_port_in', None)

        if patch_port_in:
          patchera=patch_port_in.patchera

          if patchera and 'patchera' in self.fields:
            self.initial['patchera'] = patchera.id

          if patchera and patchera.rack and 'rack' in self.fields:
            self.initial['rack'] = patchera.rack.id

        if switch_port_in:
          switch_obj = switch_port_in.switch

          if switch_obj and 'switch' in self.fields:
            self.initial['switch'] = switch_obj.id

          if switch_obj and switch_obj.rack and 'rack' in self.fields:
            self.initial['rack'] = switch_obj.rack.id

    def _filter_querysets(self):

      def get_value(fieldname):
        return self.data.get(fieldname) or self.initial.get(fieldname)

      province_id = self._to_int(get_value('province'))
      location_id = self._to_int(get_value('loation'))
      dependency_id = self._to_int(get_value('dependency'))
      edifice_id = self._to_int(get_value('edifice'))
      loc_id = self._to_int(get_value('loc'))
      office_id = self._to_int(get_value('office'))
      rack_id = self._to_int(get_value('rack'))
      patchera_id = self._to_int(get_value('patchera'))
      switch_id = self._to_int(get_value('switch'))

      if 'location' in self.fields and province_id:
        self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')

      if 'dependency' in self.fields:
        q_dependency = Dependency.objects.all()
        if location_id:
          q_dependency = q_dependency.filter(location_id=location_id)
        elif province_id:
          q_dependency = q_dependency.filter(location__province_id=province_id)
        self.fields['dependency'].queryset=q_dependency.order_by('dependency')

      if 'edifice' in self.fields:
        q_edifice = Edifice.objects.all()
        if location_id:
          q_edifice.filter(location_id=location_id)
        elif province_id:
          q_edifice.filter(location__province_id=province_id)
        self.fields['edifice'].queryset=q_edifice.order_by('edifice')

      if 'loc' in self.fields:
        q_loc = Office_Loc.objects.all()
        if edifice_id:
          q_loc = q_loc.filter(edifice_id=edifice_id)
        elif location_id:
          q_loc = q_loc.filter(edifice__location_id=location_id)
        elif province_id:
          q_loc = q_loc.filter(edifice__location__province_id=province_id)
        self.fields['loc'].queryset = q_loc.order_by('office_location')

      if 'office' in self.fields:
        q_office = Office.objects.all()
        if loc_id:
          q_office = q_office.filter(loc_id=loc_id)
        if dependency_id:
          q_office = q_office.filter(dependency_id=dependency_id)

        if edifice_id:
          q_office = q_office.filter(loc__edifice_id=edifice_id)
        elif location_id:
          q_office = q_office.filter(loc__edifice__location_id=location_id)
          q_office = q_office.filter(dependency__location_id=location_id)
        elif province_id:
          q_office = q_office.filter(loc__edifice__location__province_id=province_id)
          q_office = q_office.filter(dependency__location__province_id=province_id)
        self.fields['office'].queryset = q_office.distinct().order_by('office')

        if 'rack' in self.fields:
          q_rack = Rack.objects.all()
          if office_id:
            q_rack = q_rack.filter(office_id=office_id)
          elif location_id and province_id:
            q_rack = q_rack.filter(
              office__loc__edifice__location_id=location_id,
              office__dependency__location_id=location_id
            )
          self.fields['rack'].queryset = q_rack.order_by('rack')

        if 'patchera' in self.fields:
          q_patchera = Patchera.objects.all()
          if rack_id:
            q_patchera = q_patchera.filter(rack_id=rack_id)
          elif office_id:
            q_patchera = q_patchera.filter(rack__office_id=office_id)
          self.fields['patchera'].queryset = q_patchera.order_by('patchera')

        if 'patch_port_in' in self.fields:
          q_patch_port_in = Patch_Port.objects.all()
          if patchera_id:
            q_patch_port_in = q_patch_port_in.filter(patchera_id=patchera_id)
          elif office_id and province_id:
            q_patch_port_in = q_patch_port_in.filter(
              patchera__rack__office__loc__edifice__location__province_id=province_id,
              patchera__rack__office__dependency__location__province_id=province_id
            )
          self.fields['patch_port_in'].queryset = q_patch_port_in.order_by('port')

        if 'switch' in self.fields:
          q_switch = Switch.objects.all()
          if office_id:
            q_switch = q_switch.filter(office_id=office_id)
          if rack_id:
            q_switch = q_switch.filter(rack_id=rack_id)
          elif province_id and location_id:
            q_switch = q_switch.filter(
              office__loc__edifice__location__province_id=province_id,
              office__dependency__location__province_id=province_id
            )
          self.fields['switch'].queryset = q_switch.distinct().order_by('switch')

        if 'switch_port_in' in self.fields:
          q_switch_port_in = Switch_Port.objects.all()
          if switch_id:
            q_switch_port_in = q_switch_port_in.filter(switch_id=switch_id)
          elif office_id:
            q_switch_port_in = q_switch_port_in.filter(switch__office_id=office_id)
          self.fields['switch_port_in'].queryset = q_switch_port_in

    def _to_init(self, value):
      try:
        return int(value)
      except (ValueError, TypeError):
        return None

    def clean(self):
      cleaned_data = super().clean()
      office = cleaned_data.get('office')
      wall_port = cleaned_data.get('wall_port')
      # Verifica el constraint de unicidad
      if Wall_Port.objects.filter(office=office, wall_port=wall_port).exists():
        self.add_error('wall_port', 'Esta boca de pared ya existe en la oficina seleccionada.')
      return cleaned_data

    # def __init__(self, *args, **kwargs):
    #   super(WallPortForm, self).__init__(*args, **kwargs)

    #   if self.instance.pk:

    #     if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice and self.instance.office.loc.edifice.location and self.instance.office.loc.edifice.location.province and self.instance.office.dependency and self.instance.office.dependency.location:

    #       province = self.instance.office.loc.edifice.location.province
    #       dependency = self.instance.office.dependency
    #       location = self.instance.office.loc.edifice.location
    #       edifice = self.instance.office.loc.edifice
    #       loc = self.instance.office.loc
    #       office = self.instance.office
    #       rack = self.instance.rack
    #       patchera = self.instance.patch_port_in.patchera
    #       switch = self.instance.switch_port_in.switch
    #       patch_port = self.instance.patch_port_in
    #       switch_port = self.instance.switch_port_in

    #       self.initial['province'] = province.id
    #       self.initial['location'] = location.id
    #       self.initial['dependency'] = dependency.id
    #       self.initial['edifice'] = edifice.id
    #       self.initial['loc'] = loc.id
    #       self.initial['office'] = self.instance.office.id
    #       self.initial['rack'] = self.instance.rack.id
    #       self.initial['patchera'] = self.instance.patchera.id

    #       self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
    #       self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.office.loc.edifice.location).order_by('edifice')
    #       self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.office.dependency.location).order_by('dependency')
    #       self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.office.loc.edifice).order_by('office_location')
    #       self.fields['office'].queryset = Office.objects.filter(loc=self.instance.office.loc, dependency=self.instance.office.dependency).order_by('office')

    #       if 'province' in self.data:
    #         try:
    #           province_id = int(self.data.get('province'))
    #           self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
    #           self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
    #           self.fields['dependency'].queryet = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
    #           self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('office_location')
    #           self.fields['office'].queryset = Office.objects.filter(
    #             loc__edifice__location__province_id=province_id,
    #             dependency__location__province_id=province_id
    #             ).order_by('office')
    #           self.fields['rack'].queryset = Rack.objects.filter(
    #             office__loc__edifice__location__province_id=province_id,
    #             office__dependency__location__province_id=province_id
    #             ).order_by('rack')
    #           self.fields['patchera'].queryset = Patchera.objects.filter(
    #             rack__office__loc__edifice__location__province_id=province_id,
    #             rack__office__dependency__location__province_id=province_id
    #           ).order_by('patchera')
    #           self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
    #             patchera__rack__office__loc__edifice__location__province_id=province_id,
    #             patchera__rack__office__dependency__location__province_id=province_id
    #           ).order_by('port')
    #           self.fields['switch'].queryset = Switch.objects.filter(
    #             office__loc__edifice__location__province_id=province_id,
    #             office__dependency__location__province_id=province_id
    #           ).order_by('switch')
    #           self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
    #             switch__office__loc__edifice__location__province_id=province_id,
    #             switch__office__dependency__location__province_id=province_id
    #           )
    #           if 'rack' in self.data:
    #             self.fields['switch'].queryset = Switch.objects.filter(
    #               rack__office__loc__edifice__location__province_id=province_id,
    #               rack__office__dependency__location__province_id=province_id
    #             ).order_by('switch')
    #             self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
    #               switch__rack__office__loc__edifice__location__province_id=province_id,
    #               switch__rack__office__dependency__location__province_id=province_id
    #             ).order_by('switch_port_in')
    #         except (ValueError, TypeError):
    #           pass
    #       elif self.instance.pk:
    #         self.fields['location'].queryset = self.instance.office.loc.edifice.location.province.location_set.order_by('location')

    #       if 'location' in self.data:
    #         try:
    #           location_id = int(self.data.get('location'))
    #           self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
    #           self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id).order_by('dependency')
    #           self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=location_id).order_by('office_location')
    #           self.fields['office'].queryset = Office.objects.filter(
    #             loc__edifice__location_id=location_id,
    #             dependency__location_id=location_id
    #             ).order_by('office')
    #           self.fields['rack'].queryset = Rack.objects.filter(
    #             office__loc__edifice__location_id=location_id,
    #             office__dependency__location_id=location_id
    #             ).order_by('rack')
    #           self.fields['patchera'].queryset = Patchera.objects.filter(
    #             rack__office__loc__edifice__location_id=location_id,
    #             location_id=location_id
    #           ).order_by('patchera')
    #           self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
    #             patchera__rack__office__loc__edifice__location__location_id=location_id,
    #             patchera__rack__office__dependency__location__location_id=location_id
    #           ).order_by('port')
    #           self.fields['switch'].queryset = Switch.objects.filter(
    #             office__loc__edifice__location__location_id=location_id,
    #             office__dependency__location__location_id=location_id
    #           )
    #           self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
    #             switch__office__loc__edifice__location__location_id=location_id,
    #             switch__office__dependency__location__location_id=location_id
    #           )
    #           if 'rack' in self.data:
    #             self.fields['switch'].queryset = Switch.objects.filter(
    #               rack__office__loc__edifice__location__province_id=province_id,
    #               rack__office__dependency__location__province_id=province_id
    #             ).order_by('switch')
    #             self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
    #               switch__rack__office__loc__edifice__location__province_id=province_id,
    #               switch__rack__office__dependency__location__province_id=province_id
    #             ).order_by('switch_port_in')
    #         except (ValueError, TypeError):
    #               pass
    #       elif self.instance.pk:
    #         self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_location.order_by('edifice')
    #         self.fields['dependency'].queryset = self.instance.office.dependency.location.dependency_location.order_by('dependency')

    #       if 'dependency' in self.data:
    #         try:
    #           dependency_id = int(self.data.get('dependency'))
    #           self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id).order_by('office')
    #           self.fields['rack'].queryset = Rack.objects.filter(
    #             office__dependency__location_id=location_id
    #           ).order_by('rack')
    #           self.fields['patchera'].queryset = Patchera.objects.filter(
    #             rack__office__dependency__location_id=location_id
    #           ).order_by('patchera')
    #           self.fields['switch'].queryset = Switch.objects.filter(
    #             office__dependency__location_id=location_id
    #           ).order_by('switch')
    #           if 'rack' in self.data:
    #             self.fields['switch'].queryset = Switch.objects.filter(
    #               rack__office__dependency__location_id=location_id
    #             ).order_by('switch')
    #           elif 'patchera' in self.data:
    #             self.fields['patchera'].queryset = Switch.objects.filter(
    #               patchera__rack__office__dependency__location_id=location_id
    #             ).order_by('switch')
    #         except (ValueError, TypeError):
    #           pass
    #       elif self.instance.pk:
    #         self.fields['office'].queryset = self.instance.office.dependency.offices_dependencies.order_by('office')

    #       if 'edifice' in self.data:
    #         try:
    #           edifice_id = int(self.data.get('edifice'))
    #           self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice_id).order_by('office_location')
    #           self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=edifice_id).order_by('office')
    #           self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice_id=edifice_id).order_by('rack')
    #           self.fields['patchera'].queryset = Patchera.objects.filter(rack__loc__edifice_id=edifice_id).order_by('patchera')
    #           self.fields['switch'].queryset = Switch.objects.filter(office__loc__edifice_id=edifice_id).order_by('switch')
    #           if 'rack' in self.data:
    #             self.fields['switch'].queryset = Switch.objects.filter(rack__office__loc__edifice_id=edifice_id).order_by('switch')
    #           elif 'patchera' in self.data:
    #             self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office__loc__edifice_id=edifice_id).order_by('switch')

    #         except (ValueError, TypeError):
    #           pass
    #       elif self.instance.pk:
    #         self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_edifice.order_by('office_location')

    #       if 'loc' in self.data:
    #         try:
    #           loc_id = int(self.data.get('loc'))
    #           self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id).order_by('office')
    #           self.fields['rack'].queryset = Rack.objects.filter(office__loc_id=loc_id).order_by('rack')
    #           self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__loc_id=loc_id).order_by('patchera')
    #           self.fields['switch'].queryset = Switch.objects.filter(office__loc_id=loc_id).order_by('switch')
    #           if 'rack' in self.data:
    #             self.fields['switch'].queryset = Switch.objects.filter(rack__office__loc_id=loc_id).order_by('switch')
    #           elif 'patchera' in self.data:
    #             self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office__loc_id=loc_id).order_by('switch')
    #         except (ValueError, TypeError):
    #           pass
    #       elif self.instance.pk:
    #         self.fields['office'].queryset = self.instance.office.loc.office_location.order_by('office')

    #       if 'office' in self.data:
    #         try:
    #           office_id = int(self.data.get('office'))
    #           self.fields['rack'].queryset = Rack.objects.filter(office_id=office_id).order_by('rack')
    #           self.fields['patchera'].queryset = Patchera.objects.filter(rack__office_id=office_id).order_by('patchera')
    #           self.fields['switch'].queryset = Switch.objects.filter(office_id=office_id).order_by('switch')
    #           if 'rack' in self.data:
    #               self.fields['switch'].queryset = Switch.objects.filter(rack__office_id=office_id).order_by('switch')
    #           elif 'patchera' in self.data:
    #               self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office_id=office_id).order_by('switch')
    #         except (ValueError, TypeError):
    #           pass
    #       elif self.instance.pk:
    #         self.fields['rack'].queryset = self.instance.rack.office.rack_office.order_by('rack')

    #     if 'rack' in self.data:
    #       try:
    #         rack_id = int(self.data.get(rack))
    #         self.fields['patchera'].queryset = Patchera.objects.filter(rack_id=rack_id).order_by('patchera')
    #         self.fields['switch'].queryset = Switch.objects.filter(
    #           patchera__rack_id=rack_id,
    #           rack_id=rack_id).order_by('switch')
    #       except (ValueError, TypeError):
    #         pass
    #     elif self.instace.pk:
    #       self.fields['patchera'].queryset = self.instance.patchera.rack.patchera_rack.order_by('patchera')

    #     if 'patchera' in self.data:
    #       try:
    #         patchera_id = int(self.data.get(patchera))
    #         self.fields['switch'].queryset = Switch.objects.filter(patchera_id=patchera_id).order_by('switch')
    #       except (ValueError, TypeError):
    #         pass
    #     elif self.instace.pk:
    #       self.fields['switch'].queryset = self.instance.switch.patchera.switch_patch_port_in.order_by('switch')

    #     if office or rack:
    #       switch_filters = {}
    #       if office:
    #         switch_filters['office_id'] = office
    #       if rack:
    #         switch_filters['rack_id'] = rack
    #       self.fields['switch'].queryset = Switch.objects.filter(**switch_filters).distinct()

      # self.fields['province'].queryset = Province.objects.all()
      # self.fields['location'].queryset = Location.objects.all()
      # self.fields['dependency'].queryset = Dependency.objects.all()
      # self.fields['edifice'].queryset = Edifice.objects.all()
      # self.fields['loc'].queryset = Office_Loc.objects.all()
      # self.fields['office'].queryset = Office.objects.all()
      # self.fields['rack'].queryset = Rack.objects.all()
      # self.fields['switch_port_in'].queryset = Switch_Port.objects.all()
      # self.fields['patch_port_in'].queryset = Patch_Port.objects.all()

      # if self.instance.pk:
      #   self.initial['province'] = self.instance.office.loc.edifice.location.province
      #   self.initial['location'] = self.instance.office.loc.edifice.location
      #   self.initial['dependency'] = self.instance.office.dependency
      #   self.initial['edifice']= self.instance.office.loc.edifice
      #   self.initial['loc'] = self.instance.office.loc
      #   self.initial['office']= self.instance.office
      #   if self.instance.switch_port_in:
      #     self.initial['rack']= self.instance.switch_port_in.switch.rack
      #   elif self.patch_port_in:
      #     self.initial['rack']= self.instance.patch_port_in.patchera.rack
      #   else:
      #     'No llega a Rack'

      #   self.initial['patch_port_in'] = self.instance.patch_port_in
      #   self.initial['switch_port_in'] = self.instance.switch_port_in

      # else:
      #   selected_province = self.data.get('province')
      #   selected_location = self.data.get('location')
      #   selected_dependency = self.data.get('dependency')
      #   selected_edifice = self.data.get('edifice')
      #   selected_loc = self.data.get('loc')
      #   selected_office = self.data.get('office')
      #   selected_rack = self.data.get('rack')
      #   selected_patchera = self.data.get('patchera')
      #   selected_switch = self.data.get('switch')

      #   def to_int(value):
      #     try:
      #       return int(value)
      #     except (ValueError, TypeError):
      #       return None

      # selected_province = to_int(selected_province)
      # selected_location = to_int(selected_location)
      # selected_dependency = to_int(selected_dependency)
      # selected_edifice = to_int(selected_edifice)
      # selected_loc = to_int(selected_loc)
      # selected_office = to_int(selected_office)
      # selected_rack = to_int(selected_rack)
      # selected_patchera = to_int(selected_patchera)
      # selected_switch = to_int(selected_switch)

      # if selected_province:
      #   self.fields['location'].queryset = Location.objects.filter(province_id=selected_province)
      #   self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=selected_province)
      #   self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location__province_id=selected_province).distinct()
      #   self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=selected_province)
      #   self.fields['office'].queryset = Office.objects.filter(loc__edifice__location__province_id=selected_province)

      # if selected_location:
      #   self.fields['edifice'].queryset = Edifice.objects.filter(location_id=selected_location)
      #   self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location_id=selected_location).distinct()
      #   self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=selected_location)
      #   self.fields['office'].queryset = Office.objects.filter(loc__edifice__location_id=selected_location)

      # if selected_edifice:
      #   self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=selected_edifice)
      #   self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=selected_edifice)

      # if selected_loc:
      #   self.fields['office'].queryset = Office.objects.filter(loc_id=selected_loc)

      # if selected_dependency:
      #   self.fields['office'].queryset = self.fields['office'].queryset.filter(dependency_id=selected_dependency).distinct()

      # if selected_rack:
      #   self.fields['patchera'].queryset = Patchera.objects.filter(rack_id=selected_rack)
      #   self.fields['switch'].queryset = Switch.objects.filter(rack_id=selected_rack)

    # def clean(self):
    #   cleaned_data = super().clean()
    #   office = cleaned_data.get('office')
    #   wall_port = cleaned_data.get('wall_port')

    #   # Verifica el constraint de unicidad
    #   if Wall_Port.objects.filter(office=office, wall_port=wall_port).exists():
    #     self.add_error('wall_port', 'Esta boca de pared ya existe en la oficina seleccionada.')
    #   return cleaned_data