from django.forms import *
from django import forms
from django.forms import ModelForm, Select, TextInput, Textarea, FileInput, DateInput

from core.sh.models import Connection_Type, Dependency, Dev_Status, Device, Edifice, Location, Move_Type, Movements, Office, Office_Loc, Patch_Port, Patchera, Province, Brand, Dev_Type, Employee_Status, Employee, Rack, Suply, Suply_Type, Switch_Port, Techs, Dev_Model, Wall_Port, Switch

# Brand Forms
class BrandForm(forms.ModelForm):

  class Meta:
    model = Brand
    fields = '__all__'
    widgets = {
      'brand': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese una Marca'
        }
      )
    }

  def clean(self):
    brand = self.cleaned_data.get('brand').upper()

    if Brand.objects.filter(brand__iexact=brand).exists():
      self.add_error('brand', f"La marca ya se encuentra registrada")
    cleaned_data = super().clean()
    return cleaned_data
# Dev_Type
class Dev_TypeForm(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['dev_type'].widget.attrs['autofocus'] = True

  class Meta:
    model = Dev_Type
    fields = '__all__'
    widget = {
      'dev_type': TextInput(
        attrs={
          'placeholder': 'Ingrese un Tipo de Dispositivo'
        }
      ),
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Dev_Status
class Dev_StatusForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['dev_status'].widget.attrs['autofocus'] = True

  class Meta:
    model = Dev_Type
    fields = '__all__'
    widget = {
      'dev_status': TextInput(
        attrs={
          'placeholder': 'Ingrese un Estado para el Dispositivo'
        }
      ),
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Model
class Dev_ModelForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['dev_model'].widget.attrs['autofocus'] = True

  class Meta:
    model = Dev_Model
    fields = '__all__'
    widget = {
      'dev_type': Select(
        attrs={
          'placeholder': 'Seleccione un Tipo de Dispositivo'
        }
      ),
      'brand': Select(
        attrs={
          'placeholder': 'Seleccione una Marca'
        }
      ),
      'dev_model': TextInput(
        attrs={
          'placeholder': 'Ingrese el Modelo'
        }
      ),
      'image': FileInput(
        attrs={
          'placeholder': 'Seleccione una imagen del dispositivo'
        }
      ),
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if self.is_valid():
        self.instance = super().save(commit=commit)
        data = self.instance.toJSON()
      else:
        data['error'] = self.errors.as_json()
    except Exception as e:
      data['error'] = str(e)
    return data

# Province Forms
class ProvinceForm(forms.ModelForm):

  class Meta:
    model = Province
    fields = '__all__'
    widgets = {
      'number_id': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el número correspondiente al Distrito'
        }
      ),

      'province': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': ' Ingrese el nombre del Distrito'
        }
      )
    }

# Location Forms
class LocationForm(forms.ModelForm):

  class Meta:
    model = Location
    fields = '__all__'
    widgets = {
      'province': Select(
        attrs={
          'class': 'form-control select2',
        }
      ),

      'location': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese una localidad'
        }
      )
    }

# Edifice Forms
class EdificeForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Edifice
    fields = [
              'location', 'edifice', 'address'
              ]
    widgets = {
      'location': Select(attrs={'class': 'form-control select2'}),
      'edifice': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese un nombre identificatorio para el Edificio'
        }),
      'address': Textarea(
        attrs={
          'class': 'form-control',
          'placeholder': 'Escriba el domiclio, en caso de tener mas de uno separar por ";"'
        }
      )
    }

  def __init__(self, *args, **kwargs):
    super(EdificeForm, self).__init__(*args, **kwargs)

    self.fields['location'].queryset = Location.objects.none()

    if self.instance.pk:
      edifice = self.instance

      self.fields['location'].queryset = Location.objects.filter(
        province = self.instance.location.province
      )

    else:

      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
        except:
          pass

  def clean(self):
    edifice = self.cleaned_data.get('edifice').upper()
    location = self.cleaned_data.get('location')

    if Edifice.objects.filter(location=location, edifice=edifice).exists():
      self.add_error('edifice', f"Ya existe un edificio en el nombre '{edifice}' en la localidad seleccionada")
    cleaned_data = super().clean()
    return cleaned_data

# Dependency Forms
class DependencyForm(forms.ModelForm):

  province=forms.ModelChoiceField(
    queryset=Province.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Dependency
    fields = [
      'location', 'dependency'
    ]
    widgets = {
      'location': Select(
        attrs={
          'class': 'form-control select2'
          }),
      'dependency': TextInput(
        attrs={
          'class': 'form-control', 'placeholder': 'Ingrese la dependencia'
          }),
    }

  def __init__(self, *args, **kwargs):
    super(DependencyForm, self).__init__(*args, **kwargs)

    self.fields['location'].queryset = Location.objects.none()

    if self.instance.pk:
      dependency = self.instance

      self.fields['location'].queryset = Location.objects.filter(
        province = self.instance.location.province
      )

    else:

      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
        except:
          pass

  def clean(self):
    location = self.cleaned_data.get('location')
    dependency = self.cleaned_data.get('dependency')

    if Dependency.objects.filter(location=location, dependency=dependency).exists():
      self.add_error('dependency', f"Ya existe una dependencia con los datos ingresados")
    cleaned_data = super().clean()
    return cleaned_data
# Office Location Form
class Office_Loc_Form(forms.ModelForm):

  location=forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Office_Loc
    fields = [
      'edifice', 'floor', 'wing'
    ]
    widgets = {
      'edifice': Select(
        attrs={
          'class': 'form-control select2'
          }),
      'floor': TextInput(
        attrs={
          'class': 'form-control', 'placeholder': 'Ingre el Piso'
          }),
      'wing': TextInput(
        attrs={
          'class': 'form-control', 'placeholder': 'Ingrese el Ala'
          }),
    }
    help_texts = {
      'floor': '* Ingrese el piso ingresando 2 numeros, ej. 01, y PB para Planta baja',
      'wing': '* En caso de no haber una desigancion del ala, se recomienda ingresar el nombre de la calle a la que mira la misma'
    }

  def __init__(self, *args, **kwargs):
    super(Office_Loc_Form, self).__init__(*args, **kwargs)

    self.fields['edifice'].queryset = Edifice.objects.none()

    if self.instance.pk:
      office_loc = self.instance

      self.fields['edifice'].queryset = Edifice.objects.filter(
        location = self.instance.edifice.location
      )

    else:

      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except:
          pass

  def clean(self):
    edifice = self.cleaned_data.get('edifice')
    location = edifice.location if edifice else None
    floor = self.cleaned_data.get('floor')
    wing = self.cleaned_data.get('wing').upper()

    if Office_Loc.objects.filter(edifice=edifice, edifice__location=location, floor=floor, wing=wing).exists():
      self.add_error('floor', f"Ya existe un registro con los datos que intenta cargar")
      self.add_error('wing', f"Ya existe un registro con los datos que intenta cargar")
    cleaned_data = super().clean()
    return cleaned_data

# Office Forms
class OfficeForm(forms.ModelForm):
  location=forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  edifice=forms.ModelChoiceField(
    queryset=Edifice.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )


  class Meta:
    model = Office
    fields = [
      'edifice','dependency', 'loc', 'office', 'description'
      ]
    widgets = {
      'edifice': Select(attrs={'class': 'form-control select2'}),
      'dependency': Select(attrs={'class': 'form-control select2'}),
      'loc': Select(attrs={'class': 'form-control select2'}),
      'office': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre identificatorio para la Oficina'}),
      'description': Textarea(attrs={'class':'form-control', 'placeholder': 'Ingrese una descripción de la oficina'})
    }
    help_texts = {
      'description': '* Esta campo no es obligatorio, pero puede agregar detalles para individualizar la oficina, o agregar algún dato relevenate de la misma.'
    }

  def __init__(self, *args, **kwargs):
    super(OfficeForm, self).__init__(*args, **kwargs)

    self.fields['dependency'].queryset = Dependency.objects.none()
    self.fields['loc'].queryset = Office_Loc.objects.none()

    if self.instance.pk:
      office = self.instance

      self.fields['dependency'].queryset = Dependency.objects.filter(
        location = self.instance.dependency.location
      )

      self.fields['edifice'].queryset = Edifice.objects.filter(
        location = self.instance.loc.edifice.location
      )

      self.fields['loc'].queryset = Office_Loc.objects.filter(
        edifice = self.instance.loc.edifice
      )

    else:

      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id)
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except:
          pass

      if 'edifice'in self.data:
        try:
          edifice_id = int(self.data.get('edifice'))
          self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id)
        except:
          pass

  def clean(self):
    dependency = self.cleaned_data.get('dependency')
    office = self.cleaned_data.get('office')

    if Office.objects.filter(dependency=dependency, office__iexact=office).exists():
      self.add_error('office', f"Ya existe la oficina en la dependencia seleccionada")
    cleaned_data = super().clean()
    return cleaned_data

# Employee Status Forms
class EmployeeStatusForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['status'].widget.attrs['autofocus'] = True

  class Meta:
    model = Employee_Status
    fields = '__all__'
    widgets = {
      'status': TextInput(
        attrs={
          'placehoder': 'Ingrese un Estado para los Empleados'
        }
      )
    }

  def save(self, commit=True):
    data = {}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Employee Forms
class EmployeeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['employee_name'].widget.attrs['autofocus'] = True

  class Meta:
    model = Employee
    fields = '__all__'
    widget = {
      'employee_name': TextInput(
        attrs={
          'placeholder': 'Ingrese el Nombre del Empleado'
        }
      ),
      'employee_last_name': TextInput(
        attrs={
          'placeholder': 'Ingrese el Apellido del Empleado'
        }
      ),
      'cuil': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de CUIL'
        }
      ),
      'status': Select(
        attrs={
          'placeholder': 'Seleccione un estado'
        }
      ),
      'user_status': Select(
        attrs={
          'placeholder': 'Ingrese el usuario del empleado'
        }
      ),
      'dependency': Select(
        attrs={
          'placeholder': 'Seleccione la dependencia a la que pertenece'
        }
      ),
      'office': Select(
        attrs={
          'placeholder': 'Seleccione la oficina en que trabaja el empleado'
        }
      ),
      'avatar': FileInput(
        attrs={
          'placeholder': 'Seleccione una imagen de perfil'
        }
      ),
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Connection Type Form
class ConnectionTypeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['connection_type'].widget.attrs['autofocus'] = True

  class Meta:
    model = Connection_Type
    fields = '__all__'
    widget = {
      'connection_type': TextInput(
        attrs={
          'placeholder': 'Ingrese el Tipo de Conexión'
        }
      )
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Rack Forms
class RackForm(forms.ModelForm):

  class Meta:
    model = Rack
    fields = [
      'rack', 'details'
              ]
    widgets = {
      'rack': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el Nombre del Rack'
        }
      ),
      'details': Textarea(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese detalles que ayuden a individualizar el Rack'
        }
      )
    }
    help_texts = {
      'details': '* Aqui puede ingresar referencia de la ubicación, forma, y demas detalles que ayuden a individualizar el Rack'
    }

  def clean(self):
    rack = self.cleaned_data.get('rack').upper()

    if Rack.objects.filter(rack__iexact=rack).exists():
      self.add_error('rack', f"El Rack que se quiere ingresar, ya existe")
    cleaned_data = super().clean()
    return cleaned_data

# Patchera Forms
class PatcheraForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['patch'].widget.attrs['autofocus'] = True

  class Meta:
    model = Patchera
    fields = '__all__'
    widget = {
      'rack': Select(
        attrs={
          'placeholder': 'Seleccione el Rack donde se encuentra la Patchera'
        }
      ),
      'patch': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de orden de la patchera en el rack'
        }
      )
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Patch Port Forms
class PatchPortForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['port'].widget.attrs['autofocus'] = True

  class Meta:
    model = Patch_Port
    fields = '__all__'
    widget = {
      'patch': Select(
        attrs={
          'placeholder': 'Seleccione la Patchera'
        }
      ),
      'port': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de puerto'
        }
      )
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Switch Forms
class SwitchForm(forms.ModelForm):
  brand=forms.ModelChoiceField(
    queryset=Brand.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  model=forms.ModelChoiceField(
    queryset=Dev_Model.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  location=forms.ModelChoiceField(
    queryset=Location.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  dependency=forms.ModelChoiceField(
    queryset=Dependency.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  edifice=forms.ModelChoiceField(
    queryset=Edifice.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  class Meta:
    model = Switch
    fields = [
      'brand', 'model', 'serial_n', 'ports_q', 'rack', 'switch_rack_pos', 'office', 'dependency', 'edifice', 'location'
      ]
    widgets = {
      'serial_n': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie'}),
      'ports_q': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad de puertos del Switch'}),
      'rack': Select(attrs={'class': 'form-control select2'}),
      'switch_rack_pos': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la posición del Switch en el Rack'}),
      'office': Select(attrs={'class': 'form-control select2'}),
      'dependency': Select(attrs={'class': 'form-control select2'}),
      'edifice': Select(attrs={'class': 'form-control select2'}),
      'location': Select(attrs={'class': 'form-control select2'})
    }
    help_texts = {
      'ports_q': '* Ingrese solo números',
      'switch_rack_pos': '* Ingrese el número de posición del switch en el rack'
    }

  def __init__(self, *args, **kwargs):
    super(SwitchForm, self).__init__(*args, **kwargs)

    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['model'].queryset = Dev_Model.objects.all()
    self.fields['office'].queryset = Office.objects.all()
    self.fields['dependency'].queryset = Dependency.objects.all()
    self.fields['edifice'].queryset = Edifice.objects.all()
    self.fields['location'].queryset = Location.objects.all()
    self.fields['rack'].queryset = Rack.objects.all()

    if self.instance.pk:
      switch = self.instance

      dev_type = self.instance.model.dev_type
      self.fields['brand'].queryset = Brand.objects.filter(dev_model__dev_type=dev_type).distinct()
      self.fields['brand'].initial = self.instance.model.brand

      if self.instance.model:
        self.fields['model'].queryset = Dev_Model.objects.filter(
        dev_type = dev_type,
        brand = self.instance.model.brand
      )

      if self.instance.office:
        location = self.instance.office.edifice.location
        self.fields['location'].initial = location
        self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
        self.fields['edifice'].initial = self.instance.office.edifice
        self.fields['dependency'].queryset = Dependency.objects.filter(location=location)
        self.fields['dependency'].initial = self.instance.office.dependency
        self.fields['office'].queryset = Office.objects.filter(
          edifice = self.instance.office.edifice,
          dependency = self.instance.office.dependency
        )
        self.fields['office'].initial = self.instance.office

  def clean(self):
    cleaned_data = super().clean()
    model = self.cleaned_data.get('model')
    serial_n = self.cleaned_data.get('serial_n')
    rack = self.cleaned_data.get('rack')
    switch_rack_pos = self.cleaned_data.get('switch_rack_pos')

    if Switch.objects.filter(model=model, serial_n=serial_n).exists():
      self.add_error('model', f"Ya se encuentra cargado este modelo de Switch")
      self.add_error('serial_n', f"El número de serie ya se encuentra registrado y asociado al mismo modelo")
    if Switch.objects.filter(rack=rack, switch_rack_pos=switch_rack_pos).exists():
      self.add_error('rack', f"El switch ya se encuentra en el Rack seleccionado")
      self.add_error('switch_rack_pos', f"La posicion seleccionada en el Rack, ya se encuentra ocupada")
    return cleaned_data


# Switch Port Forms
class SwitchPortForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['port_id'].widget.attrs['autofocus'] = True

  class Meta:
    model = Switch_Port
    fields = '__all__'
    widget = {
      'switch': Select(
        attrs={
          'placeholder': 'Seleccione el Switch'
        }
      ),
      'port_id': TextInput(
        attrs={
          'placeholder': 'Ingrese el número de puerto'
        }
      ),
      'patch_port_out': Select(
        attrs={
          'placeholder': 'Seleccione el puerto de la patchera a la que sale el puerto'
        }
      ),
      'patch_port_in': Select(
        attrs={
          'placeholder': 'Seleccione el puerto de la patchera desde la que ingresa la conexion'
        }
      ),
      'switch_in': Select(
        attrs={
          'placeholder': 'Seleccione el switch padre'
        }
      ),
      'switch_out': Select(
        attrs={
          'placeholder': 'En caso de existir, seleccione el switch hijo'
        }
      ),
      'obs': Textarea(
        attrs={
          'placeholder': 'Ingrese detalles particulares, si los hubiese'
        }
      )
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Wall Port Forms
class WallPortForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['wall_port'].widget.attrs['autofocus'] = True

  class Meta:
      model = Wall_Port
      fields = '__all__'
      widget = {
        'office': Select(
          attrs={
            'placeholder': 'Seleccione la Oficina'
          }
        ),
        'wall_port': TextInput(
          attrs={
            'placeholder': 'Ingrese el puerto/boca de la pared'
          }
        ),
        'patch_port': Select(
          attrs={
            'placeholder': 'Seleccione el puerto de la patchera de origen'
          }
        ),
        'switch_port_in': Select(
          attrs={
            'placeholder': 'En caso de ser conexion directa, seleccione el puerto del switch de origen'
          }
        ),
        'switch_out': Select(
          attrs={
            'placeholder': 'En caso de extender la boca, seleccione el switch hijo'
          }
        ),
        'details': Textarea(
          attrs={
            'placeholder': 'De ser necesario, ingrese detalles particulares'
          }
        )
      }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Device Forms

class DeviceForm(forms.ModelForm):

  brand = forms.ModelChoiceField(
    queryset=Brand.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  dev_type = forms.ModelChoiceField(
    queryset=Dev_Type.objects.all(),
    widget=forms.Select(attrs={'class':'form-control select2'}),
    required=False
  )

  dev_model = forms.ModelChoiceField(
    queryset=Dev_Model.objects.none(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=True
  )

  dependency = forms.ModelChoiceField(
    queryset=Dependency.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control select2'}),
    required=False
  )

  class Meta:
    model = Device
    fields = [
      'dev_model', 'connection', 'ip', 'net_name', 'dev_status', 'serial_n', 'office', 'wall_port', 'switch_port', 'employee'
    ]
    widgets = {
      'connection': Select(attrs={'class': 'form-control select2'}),
      'ip': TextInput(attrs={'class': 'form-control', 'placeholder': 'Si tuviera, ingrese la dirección ip del dispositivo'}),
      'net_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Si tuviera, ingrese el nombre de registro en la red del dispositivo'}),
      'dev_status': Select(attrs={'class': 'form-control select2'}),
      'serial_n': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie'}),
      'office': Select(attrs={'class': 'form-control select2'}),
      'wall_port': Select(attrs={'class': 'form-control select2'}),
      'switch_port': Select(attrs={'class': 'form-control select2'}),
      'employee': SelectMultiple(attrs={'class': 'form-control select2'}),
    }

  def __init__(self, *args, **kwargs):
    super(DeviceForm, self).__init__(*args, **kwargs)

    self.fields['dev_model'].queryset = Dev_Model.objects.none()
    self.fields['office'].queryset = Office.objects.none()
    self.fields['wall_port'].queryset = Wall_Port.objects.none()
    self.fields['switch_port'].queryset = Switch_Port.objects.none()
    self.fields['employee'].queryset = Employee.objects.none()

    if self.instance.pk:
      device = self.instance

      self.fields['dev_model'].queryset = Dev_Model.objects.filter(
        brand = self.instance.dev_model.brand,
        dev_type = self.instance.dev_model.dev_type
      )

      self.fields['office'].queryset = Office.objects.filter(
        dependency = self.instance.office.dependency
      )

      self.fields['wall_port'].queryset = Wall_Port.objects.filter(office=self.instance.office)
      self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office=self.instance.office)
      self.fields['employee'].queryset = Employee.objects.filter(office=self.instance.office)

    else:

      if 'dependency' in self.data:
        try:
          dependency_id = int(self.data.get('dependency'))
          self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id)
        except:
          pass

      if 'office' in self.data:
        try:
          office_id = int(self.data.get('office'))
          self.fields['wall_port'].queryset = Wall_Port.objects.filter(office_id=office_id)
          self.fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office_id=office_id)
          self.fields['employee'].queryset = Employee.objects.filter(office_id=office_id)
        except (ValueError, TypeError):
          pass

      if 'brand' in self.data and 'dev_type' in self.data:
        try:
          brand_id = int(self.data.get('brand'))
          dev_type_id = int(self.data.get('dev_type'))
          self.fields['dev_model'].queryset = Dev_Model.objects.filter(brand_id=brand_id, dev_type_id=dev_type_id)
        except (ValueError, TypeError):
          pass

  def clean(self):
    cleaned_data = super().clean()
    print("cleaned data: ", cleaned_data)
    return cleaned_data

# Techs
class TechsForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['last_name'].widget.attrs['autofocus'] = True

  class Meta:
    model = Techs
    fields = '__all__'
    widget = {
      'name': TextInput(
        attrs={
          'placeholder': 'Ingrese el nombre del Técnico'
        }
      ),
      'last_name': TextInput(
        attrs={
          'placeholder': 'Ingrese el apellido del Técnico'
        }
      )
    }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Suply_Type
class SuplyTypeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['suply_type'].widget.attrs['autofocus'] = True

  class Meta:
      model = Suply_Type
      fields = '__all__'
      widget = {
        'suply_type': TextInput(
          attrs={
            'placeholder': 'Ingrese el tipo de insumo'
          }
        )
      }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Suply
class SuplyForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['serial_suply'].widget.attrs['autofocus'] = True

  class Meta:
      model = Suply
      fields = '__all__'
      widget = {
        'suply_type': Select(
          attrs={
            'placeholder': 'Seleccione el tipo de insumo'
          }
        ),
        'dev_model': Select(
          attrs={
            'placeholder': 'Seleccione para que dispositivo es el insumo'
          }
        ),
        'serial_suply': TextInput(
          attrs={
            'placeholder': 'Ingrese el número de serie del insumo'
          }
        ),
        'date_in': DateInput(
          attrs={
            'placeholder': 'Ingrese la fecha de ingreso al stock del insumo'
          }
        )
      }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Move Type
class MoveTypeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['move'].widget.attrs['autofocus'] = True

  class Meta:
      model = Move_Type
      fields = '__all__'
      widget = {
        'move': TextInput(
          attrs={
            'placeholder': 'Ingrese el tipo de movimiento'
          }
        )
      }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

# Movements
class MovementsForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['port_id'].widget.attrs['autofocus'] = True

  class Meta:
      model = Movements
      fields = '__all__'
      widget = {
        'device': Select(
          attrs={
            'placeholder': 'Seleccione un dispositivo'
          }
        ),
        'port_id': Select(
          attrs={
            'placeholder': 'Seleccione el tipo de movimiento'
          }
        ),
        'techs': Select(
          attrs={
            'placeholder': 'Seleccione el Técnico responsable del movimiento'
          }
        ),
        'date': DateInput(
          attrs={
            'placeholder': 'Ingrese la fecha del movimiento'
          }
        ),
        'suply': Select(
          attrs={
            'placeholder': 'En caso de haberse requerido, ingrese el insumo utilizado'
          }
        ),
        'detail': Textarea(
          attrs={
            'placeholder': 'Describa el detalle del movimiento realizado'
          }
        ),
      }

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

