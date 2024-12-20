class SwitchForm(forms.ModelForm):
  # Campos comunes para ambos caminos
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

  # Campos para la ubicación del switch
  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
    required = False
  )

  dependency = forms.ModelChoiceField(
    queryset = Dependency.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
    required = False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
    required = False
  )

  # Campos para la conexión de entrada
  edifice_ports = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice_ports'}),
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

  # Otros campos existentes
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

  class Meta:
    model = Switch
    fields = [
      'brand', 'model', 'serial_n', 'ports_q', 'rack', 'switch_rack_pos', 
      'office', 'wall_port_in', 'switch_port_in', 'patch_port_in'
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

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Inicializar querysets base
    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['model'].queryset = Dev_Model.objects.filter(dev_type__dev_type='SWITCH')

    if 'province' in self.data:
      try:
        province_id = int(self.data.get('province'))
        # Filtrar locations por provincia
        self.fields['location'].queryset = Location.objects.filter(
          province_id=province_id
        ).order_by('location')
      except (ValueError, TypeError):
        pass

    if 'location' in self.data:
      try:
        location_id = int(self.data.get('location'))
        # Filtrar edificios y dependency para ambos caminos
        self.fields['edifice'].queryset = Edifice.objects.filter(
          location_id=location_id
        ).order_by('edifice')
        self.fields['edifice_ports'].queryset = Edifice.objects.filter(
          location_id=location_id
        ).order_by('edifice')
        self.fields['dependency'].queryset = Dependency.objects.filter(
          location_id=location_id
        ).order_by('dependency')
      except (ValueError, TypeError):
        pass

    # Camino para la ubicación del switch
    if 'edifice' in self.data:
      try:
        edifice_id = int(self.data.get('edifice'))
        self.fields['loc'].queryset = Office_Loc.objects.filter(
          edifice_id=edifice_id
        ).order_by('office_location')
        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice_id=edifice_id
        ).order_by('office')
        self.fields['rack'].queryset = Rack.objects.filter(
          office__loc__edifice_id=edifice_id
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    # Camino para los puertos
    if 'edifice_ports' in self.data:
      try:
        edifice_ports_id = int(self.data.get('edifice_ports'))
        self.fields['loc_ports'].queryset = Office_Loc.objects.filter(
          edifice_id=edifice_ports_id
        ).order_by('office_location')
      except (ValueError, TypeError):
        pass

    if 'loc_ports' in self.data:
      try:
        loc_ports_id = int(self.data.get('loc_ports'))
        self.fields['office_ports'].queryset = Office.objects.filter(
          loc_id=loc_ports_id
        ).order_by('office')
        self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
          office__loc_id=loc_ports_id
        ).order_by('wall_port_in')
      except (ValueError, TypeError):
        pass

    if 'office_ports' in self.data:
      try:
        office_ports_id = int(self.data.get('office_ports'))
        self.fields['rack_ports'].queryset = Rack.objects.filter(
          office_id=office_ports_id
        ).order_by('rack')
      except (ValueError, TypeError):
        pass

    if 'rack_ports' in self.data:
      try:
        rack_ports_id = int(self.data.get('rack_ports'))
        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
          switch__rack_id=rack_ports_id
        ).order_by('switch_port_in')
        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(
          patchera__rack_id=rack_ports_id
        ).order_by('patch_port_in')
      except (ValueError, TypeError):
        pass

    # Similar logic for edit mode
    if self.instance.pk:
      if self.instance.office:
        # Set querysets for switch location path
        self.fields['location'].queryset = self.instance.office.loc.edifice.location.province.location_set.order_by('location')
        self.fields['edifice'].queryset = self.instance.office.loc.edifice.location.edifice_set.order_by('edifice')
        self.fields['dependency'].queryset = self.instance.office.dependency.location.dependency_set.order_by('dependency')
        self.fields['loc'].queryset = self.instance.office.loc.edifice.office_loc_set.order_by('office_location')
        self.fields['office'].queryset = self.instance.office.loc.office_set.order_by('office')
        
        # Set querysets for ports path if they exist
        if hasattr(self.instance, 'wall_port_in') and self.instance.wall_port_in:
          self.fields['edifice_ports'].queryset = self.instance.wall_port_in.office.loc.edifice.location.edifice_set.order_by('edifice')
          self.fields['loc_ports'].queryset = self.instance.wall_port_in.office.loc.edifice.office_loc_set.order_by('office_location')
          self.fields['office_ports'].queryset = self.instance.wall_port_in.office.loc.office_set.order_by('office')

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

# from django.db import models
# from django.forms import model_to_dict

# from core.sh.models.patch_port.models import Patch_Port
# from core.sh.models.wall_port.models import Wall_Port

# from ..dev_model.models import Dev_Model
# from ..dev_type.models import Dev_Type
# from ..office.models import Office
# from ..rack.models import Rack

# class Switch(models.Model):
#   model = models.ForeignKey(Dev_Model, related_name = 'switch_model', verbose_name = 'Modelo', on_delete = models.CASCADE)
#   serial_n = models.CharField(max_length = 20, verbose_name='N° de Serie', null = True, blank = True)
#   ports_q = models.CharField(max_length = 2, verbose_name = 'Cantidad de Puertos')
#   rack = models.ForeignKey(Rack, related_name = 'switch_rack', verbose_name = 'Rack', on_delete = models.CASCADE, null = True, blank = True)
#   switch_rack_pos = models.CharField(max_length = 2, verbose_name = 'Posición en el Rack', blank=True, null=True)
#   office = models.ForeignKey(Office, related_name = 'switch_office', verbose_name = 'Oficina', on_delete = models.CASCADE, blank=True, null=True)
#   wall_port_in = models.OneToOneField('sh.Wall_Port', related_name='switch_wall_port_in', verbose_name='Boca de la pared', on_delete=models.CASCADE, blank=True, null=True)
#   switch_port_in = models.OneToOneField('sh.Switch_Port', related_name='switch_switch_port_in', verbose_name='Puerto de Switch', on_delete=models.CASCADE, blank=True, null=True)
#   patch_port_in = models.OneToOneField('sh.Patch_Port', related_name='switch_patch_port_in', verbose_name='Puerto de patchera de Entrada', on_delete=models.CASCADE, blank=True, null=True)
#   date_creation = models.DateTimeField(auto_now_add = True, verbose_name = 'Fecha de Registro')
#   date_updated = models.DateTimeField(auto_now = True, verbose_name = 'Última Modificación')

#   def save(self,*args, **kwargs):
#     try:
#       switch_dev_type = Dev_Type.objects.get(dev_type = 'SWITCH')
#     except Dev_Type.DoesNotExist:
#       switch_dev_type = Dev_Type.objects.create(dev_type = 'SWITCH')
#     except Dev_Type.MultipleObjectsReturned:
#       switch_dev_type = Dev_Type.objects.filter(dev_type = 'SWITCH').first()

#     if self.model.dev_type != switch_dev_type:
#       self.model.dev_type = switch_dev_type
#       self.model.dev_type.save()
#       self.model.save()

#     if self.serial_n:
#       self.serial_n = self.serial_n.upper()
#     if self.switch_rack_pos:
#       self.switch_rack_pos = self.switch_rack_pos.upper()

#     super(Switch, self).save(*args, **kwargs)

#   def __str__(self):
#     if self.rack:
#       return f'{self.model.brand.brand} {self.model.dev_model} DE {self.ports_q} PUERTOS / POSICION {self.switch_rack_pos} / RACK {self.rack} /  OFICINA {self.rack.office}'
#     else:
#       return f'{self.model.brand.brand} DE {self.ports_q} PUERTOS / {self.serial_n} EN LA OFICINA / {self.office} / SIN RACK'

#   def toJSON(self):
#     item = model_to_dict(self)
#     item['brand'] = self.model.brand.brand if self.model and self.model.brand else 'GENÉRICO'
#     item['serial_n'] = self.serial_n if self.serial_n else 'GENÉRICO SIN S/N°'
#     item['ports_q'] = self.ports_q
#     item['rack'] = self.rack.rack if self.rack else 'NO ESTA EN RACK'
#     item['office'] = self.office.office if self.office else 'NO ESTA EN UNA OFICINA'
#     item['switch_rack_pos'] = self.switch_rack_pos if self.rack else 'NO ESTA EN RACK'
#     return item

#   class Meta:
#     verbose_name = 'Switch'
#     verbose_name_plural = 'Switches'
#     db_table = 'switchs'
#     ordering = ['id']
#     constraints = [
#       models.UniqueConstraint(fields=['model', 'serial_n'], name='unique_model_serial'),
#       models.UniqueConstraint(fields=['rack', 'switch_rack_pos'], name='unique_rack_switch_rack_pos')
#     ]