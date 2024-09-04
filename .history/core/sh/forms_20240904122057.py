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
# Dev_Type
class Dev_TypeForm(ModelForm):

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

  class Meta:
    model = Dependency
    fields = '__all__'
    widgets = {
      'dependency': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese el Nombre de una Dependencia'
        }
      ),
    }

  def clean_dependency(self):
    dependency = self.cleaned_data.get('dependency')

    if Dependency.objects.filter(dependency__iexact=dependency).exists():
      raise ValidationError("Esta dependencia ya existe")

    return dependency

# Office Loc Form
class OfficeLocForm(forms.ModelForm):
  province = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = True
  )


  class Meta:
    model = Office_Loc
    fields = [
      'edifice', 'floor', 'wing'
    ]
    widgets = {
      'floor': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el piso'}),
      'wing': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el nombre del ala'
      })
    }
    help_texts = {
      'wing': 'En caso de no tener un nombre de ala se recomienda poner el nombre de la calle hacia la que mira el ala.'
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.fields['location'].queryset = Location.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()

    if self.instance.pk:
      office_loc = self.instance

      self.fields['location'].queryset = Location.objects.filter(
        province = self.instance.location.province
      )

      self.fields['edifice'].queryset = Edifice.objects.filter(
        province = self.instance.edifice.location.province,
        location = self.instance.edifice.location
      )

    else:
      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.fileter(province_id=province_id)
        except:
          pass

      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except:
          pass

  def clean(self):
    cleaned_data = super().clean()
    print("cleaned data: ", cleaned_data)
    return cleaned_data


# Office Forms
class OfficeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['office'].widget.attrs['autofocus'] = True

  class Meta:
    model = Office
    fields = '__all__'
    widget = {
      'edifice': Select(
        attrs={
          'placeholder': 'Seleccione un Edificio'
        }
      ),
      'office': TextInput(
        attrs={
          'placeholder': 'Ingrese un nombre identificatorio para la Oficina'
        }
      ),
      'dependency': Select(
        attrs={
          'placeholder': 'Seleccione una Dependencia'
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
class RackForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['rack'].widget.attrs['autofocus'] = True

  class Meta:
    model = Rack
    fields = '__all__'
    widget = {
      'rack': TextInput(
        attrs={
          'placeholder': 'Ingrese el Nombre del Rack'
        }
      ),
      'details': Textarea(
        attrs={
          'placeholder': 'Ingrese detalles que ayuden a individualizar el Rack'
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
class SwitchForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['switch_rack_pos'].widget.attrs['autofocus'] = True

  class Meta:
      model = Switch
      fields = '__all__'
      widget = {
        'brand': Select(
          attrs={
            'placeholder': 'Seleccione la marca del Switch'
          }
        ),
        'serial_n': TextInput(
          attrs={
            'placeholder': 'Ingrese el número de serie'
          }
        ),
        'ports_q': TextInput(
          attrs={
            'placeholder': 'Ingrese la cantidad de puertos del Switch'
          }
        ),
        'rack': Select(
          attrs={
            'placeholder': 'Seleccione el Rack donde está instalado el Switch'
          }
        ),
        'switch_rack_pos': TextInput(
          attrs={
            'placeholder': 'Ingrese la posición del Switch en el Rack'
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
      'connection': forms.Select(attrs={'class': 'form-control select2'}),
      'ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Si tuviera, ingrese la dirección ip del dispositivo'}),
      'net_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Si tuviera, ingrese el nombre de registro en la red del dispositivo'}),
      'dev_status': forms.Select(attrs={'class': 'form-control select2'}),
      'serial_n': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie'}),
      'office': forms.Select(attrs={'class': 'form-control select2'}),
      'wall_port': forms.Select(attrs={'class': 'form-control select2'}),
      'switch_port': forms.Select(attrs={'class': 'form-control select2'}),
      'employee': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
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

