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

              self.fields = ['location'].queryset = Location.objects.filter(
                    province_id=province_id
                    ).order_by('location')
              self.fields = ['edifice'].queryset = Edifice.objects.filter(
                    location__province_id=province_id
                    ).order_by('edifice')
              self.fields = ['dependency'].queryset = Dependency.objects.filter(
                    location__province_id=province_id
                    ).order_by('dependency')
              self.fields = ['loc'].queryset = Office_Loc.objects.filter(
                    edifice__location__province_id=province_id
                    ).order_by('loc')
              self.fields = ['office'].queryset = Office.objects.filter(
                    loc__edifice__location__province_id=province_id
                    ).order_by('office')
              self.fields = ['rack'].queryset = Rack.objects.filter(
                    office__loc__edifice__location__province_id=province_id
                    ).order_by('rack')
              self.fields = ['switch'].queryset = Switch.objects.filter(
                    office__loc__edifice__location__province_id=province_id,
                    rack__office__loc__edifice__location__province_id=province_id
                    ).order_by('switch')
              self.fields = ['patchera'] = Patchera.objects.filter(
                  rack__office__loc__edifice__location__province_id=province_id).order_by('patchera')
              self.fields = ['switch_port_in'].queryset = Switch_Port.objects.filter(
                    switch__office__loc__edifice__location__province_id=province_id,
                    switch__rack__office__loc__edifice__location__province_id=province_id
                    ).order_by('port_id')
              self.fields = ['patch_port_in'] = Patch_Port.objects.filter(
                    patchera__rack__office__loc__edifice__location__province_id=province_id
                  )
            except (ValueError, TypeError):
              pass

          if 'location' in self.data:
#!CONTINUAR DESDE AQUI 

    #   self._set_initial_data_from_instance()
    #   self._filter_querysets()

    #   for field_name, field in self.fields.items():
    #     if field_name in self.initial:
    #       preselected_value = self.initial[field_name]
    #       if hasattr(field.widget, 'attrs'):
    #         field.widget.attrs['data-preselected'] = str(preselected_value)

    # def _set_initial_data_from_instance(self):

    #   if not self.instance.pk:
    #     return

    #   instance = self.instance

    #   office = getattr(instance, 'office', None)
    #   if office and hasattr(office, 'loc') and office.loc and hasattr(office.loc, 'edifice') and office.loc.edifice and hasattr(office.loc.edifice, 'location') and office.dependency and office.dependency.location:

    #     province = office.loc.edifice.location.province
    #     dependency = office.dependency
    #     location = office.loc.edifice.location
    #     edifice = office.loc.edifice
    #     loc = office.loc

    #     if 'province' in self.fields and province:
    #       self.initial['province'] = province.id
    #     if 'location' in self.fields and location:
    #       self.initial['location'] = location.id
    #     if 'dependency' in self.fields and dependency:
    #       self.initial['dependency'] = dependency.id
    #     if 'edifice' in self.fields and edifice:
    #       self.initial['edifice'] = edifice.id
    #     if 'loc' in self.fields and loc:
    #       self.initial['loc'] = loc.id
    #     if 'office' in self.fields and office:
    #       self.initial['office'] = office.id

    #     rack = getattr(instance, 'rack', None)
    #     patch_port_in = getattr(instance, 'patch_port_in', None)
    #     switch_port_in = getattr(instance, 'switch_port_in', None)
    #     patchera = patch_port_in.patchera if patch_port_in else None
    #     switch_obj = switch_port_in.switch if switch_port_in else None

    #     if 'rack' in self.fields and rack:
    #       self.initial['rack'] = rack.id
    #     if 'patchera' in self.fields and patchera:
    #       self.initial['patchera'] = patchera.id
    #     if 'switch' in self.fields and switch_obj:
    #       self.initial['switch'] = switch_obj.id

    #     patch_port_in = getattr(instance, 'patch_port_in', None)
    #     switch_port_in = getattr(instance, 'switch_port_in', None)

    #     if patch_port_in:
    #       patchera=patch_port_in.patchera

    #       if patchera and 'patchera' in self.fields:
    #         self.initial['patchera'] = patchera.id

    #       if patchera and patchera.rack and 'rack' in self.fields:
    #         self.initial['rack'] = patchera.rack.id

    #     if switch_port_in:
    #       switch_obj = switch_port_in.switch

    #       if switch_obj and 'switch' in self.fields:
    #         self.initial['switch'] = switch_obj.id

    #       if switch_obj and switch_obj.rack and 'rack' in self.fields:
    #         self.initial['rack'] = switch_obj.rack.id

    # def _filter_querysets(self):

    #   def get_value(fieldname):
    #     return self.data.get(fieldname) or self.initial.get(fieldname)

    #   province_id = self.initial.get('province')
    #   location_id = self._to_int(get_value('location'))
    #   dependency_id = self._to_int(get_value('dependency'))
    #   edifice_id = self._to_int(get_value('edifice'))
    #   loc_id = self._to_int(get_value('loc'))
    #   office_id = self._to_int(get_value('office'))
    #   rack_id = self._to_int(get_value('rack'))
    #   patchera_id = self._to_int(get_value('patchera'))
    #   switch_id = self._to_int(get_value('switch'))

    #   if 'location' in self.fields and province_id:
    #     self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')

    #   if 'dependency' in self.fields:
    #     q_dependency = Dependency.objects.all()
    #     if location_id:
    #       q_dependency = q_dependency.filter(location_id=location_id)
    #     elif province_id:
    #       q_dependency = q_dependency.filter(location__province_id=province_id)
    #     self.fields['dependency'].queryset=q_dependency.order_by('dependency')

    #   if 'edifice' in self.fields:
    #     q_edifice = Edifice.objects.all()
    #     if location_id:
    #       q_edifice.filter(location_id=location_id)
    #     elif province_id:
    #       q_edifice.filter(location__province_id=province_id)
    #     self.fields['edifice'].queryset=q_edifice.order_by('edifice')

    #   if 'loc' in self.fields:
    #     q_loc = Office_Loc.objects.all()
    #     if edifice_id:
    #       q_loc = q_loc.filter(edifice_id=edifice_id)
    #     elif location_id:
    #       q_loc = q_loc.filter(edifice__location_id=location_id)
    #     elif province_id:
    #       q_loc = q_loc.filter(edifice__location__province_id=province_id)
    #     self.fields['loc'].queryset = q_loc.order_by('office_location')

    #   if 'office' in self.fields:
    #     q_office = Office.objects.all()
    #     if loc_id:
    #       q_office = q_office.filter(loc_id=loc_id)
    #     if dependency_id:
    #       q_office = q_office.filter(dependency_id=dependency_id)

    #     if edifice_id:
    #       q_office = q_office.filter(loc__edifice_id=edifice_id)
    #     elif location_id:
    #       q_office = q_office.filter(loc__edifice__location_id=location_id)
    #       q_office = q_office.filter(dependency__location_id=location_id)
    #     elif province_id:
    #       q_office = q_office.filter(loc__edifice__location__province_id=province_id)
    #       q_office = q_office.filter(dependency__location__province_id=province_id)
    #     self.fields['office'].queryset = q_office.distinct().order_by('office')

    #     if 'rack' in self.fields:
    #       q_rack = Rack.objects.all()
    #       if office_id:
    #         q_rack = q_rack.filter(office_id=office_id)
    #       if loc_id:
    #         q_rack = q_rack.filter(office__loc_id=loc_id)
    #       if edifice_id:
    #         q_rack = q_rack.filter(office__loc__edifice_id=edifice_id)
    #       if dependency_id:
    #         q_rack = q_rack.filter(office__dependency_id=dependency_id)
    #       if location_id:
    #         q_rack = q_rack.filter(
    #           office__loc__edifice__location_id=location_id,
    #           office__dependency__location_id=location_id
    #         )
    #       if province_id:
    #         q_rack = q_rack.filter(
    #           office__loc__edifice__location__province_id=province_id,
    #           office__dependency__location__province_id=province_id
    #         )
    #       self.fields['rack'].queryset = q_rack.order_by('rack')

    #     if 'patchera' in self.fields:
    #       q_patchera = Patchera.objects.all()
    #       if rack_id:
    #         q_patchera = q_patchera.filter(rack_id=rack_id)
    #       elif office_id:
    #         q_patchera = q_patchera.filter(rack__office_id=office_id)
    #       self.fields['patchera'].queryset = q_patchera.order_by('patchera')

    #     if 'patch_port_in' in self.fields:
    #       q_patch_port_in = Patch_Port.objects.all()
    #       if patchera_id:
    #         q_patch_port_in = q_patch_port_in.filter(patchera_id=patchera_id)
    #       elif office_id and province_id:
    #         q_patch_port_in = q_patch_port_in.filter(
    #           patchera__rack__office__loc__edifice__location__province_id=province_id,
    #           patchera__rack__office__dependency__location__province_id=province_id
    #         )
    #       self.fields['patch_port_in'].queryset = q_patch_port_in.order_by('port')

    #     if 'switch' in self.fields:
    #       q_switch = Switch.objects.all()
    #       if office_id:
    #         q_switch = q_switch.filter(office_id=office_id)
    #       if rack_id:
    #         q_switch = q_switch.filter(rack_id=rack_id)
    #       elif province_id and location_id:
    #         q_switch = q_switch.filter(
    #           office__loc__edifice__location__province_id=province_id,
    #           office__dependency__location__province_id=province_id
    #         )
    #       self.fields['switch'].queryset = q_switch.distinct().order_by('switch')

    #     if 'switch_port_in' in self.fields:
    #       q_switch_port_in = Switch_Port.objects.all()
    #       if switch_id:
    #         q_switch_port_in = q_switch_port_in.filter(switch_id=switch_id)
    #       elif office_id:
    #         q_switch_port_in = q_switch_port_in.filter(switch__office_id=office_id)
    #       self.fields['switch_port_in'].queryset = q_switch_port_in

    # def _to_init(self, value):
    #   try:
    #     return int(value)
    #   except (ValueError, TypeError):
    #     return None

    # def clean(self):
    #   cleaned_data = super().clean()
    #   office = cleaned_data.get('office')
    #   wall_port = cleaned_data.get('wall_port')
    #   # Verifica el constraint de unicidad
    #   if Wall_Port.objects.filter(office=office, wall_port=wall_port).exists():
    #     self.add_error('wall_port', 'Esta boca de pared ya existe en la oficina seleccionada.')
    #   return cleaned_data