from django.forms import *
from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm, Select, TextInput, Textarea, FileInput, DateInput, RadioSelect
from django.forms.utils import ErrorList

from core.sh.models import Connection_Type, Dependency, Device, Edifice, Location, Move_Type, Movements, Office, Patch_Port, Patchera, Province, Brand, Dev_Type, Employee_Status, Employee, Rack, Suply, Suply_Type, Switch_Port, Techs, Dev_Model, Wall_Port, Switch

# Brand Forms
class BrandForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['brand'].widget.attrs['autofocus'] = True

  class Meta:
    model = Brand
    fields = '__all__'
    widget = {
      'brand': TextInput(
        attrs={
          'placeholder': 'Ingrese el Nombre de una Marca'
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
class ProvinceForm(ModelForm):

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for form in self.visible_fields():
        form.field.widget.attrs['class'] = 'form-control m-1'
      self.fields['number_id'].widget.attrs['autofocus'] = True


  class Meta:
    model = Province
    fields = '__all__'
    widgets = {
      'number_id': TextInput(
        attrs={
          'placeholder': 'Ingrese el número correspondiente al Distrito'
        }
      ),

      'province': TextInput(
        attrs={
          'placeholder': ' Ingrese el nombre del Distrito'
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

# Location Forms
class LocationForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['location'].widget.attrs['autofocus'] = True

  class Meta:
    model = Location
    fields = '__all__'
    widget = {
      'Province': Select(
        attrs={
          'placeholder': 'Seleccione la Provincia'
        }
      ),
      'Location': TextInput(
        attrs={
          'placeholder': 'Ingrese el nombre de la Localidad'
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

# Edifice Forms
class EdificeForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['edifice'].widget.attrs['autofocus'] = True

  class Meta:
    model = Edifice
    fields = '__all__'
    widget = {
      'location': Select(
        attrs={
          'placeholder': 'Seleccione la Localidad'
        }
      ),
      'edifice': TextInput(
        attrs={
          'placeholder': 'Ingrese un nombre identificatorio para el Edificio'
        }
      ),
      'address': Textarea(
        attrs={
          'placeholder': 'Escriba el domiclio, en caso de tener mas de uno separar por ";"'
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

# Dependency Forms
class DependencyForm(ModelForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control m-1'
    self.fields['description'].widget.attrs['autofocus'] = True

  class Meta:
    model = Dependency
    fields = '__all__'
    widget = {
      'description': TextInput(
        attrs={
          'placeholder': 'Ingrese el Nombre de una Dependencia'
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

class DeviceForm(Form):

  class Meta:
    dev_type = ModelChoiceField(
      queryset = Dev_Type.objects.all(), widget = Select(
        attrs = {
          'class': 'form-control select2',
          'paceholder': 'Seleccione el tipo de dispositivo'
        }
      )
    )
    dev_model = ModelChoiceField(
      queryset = Dev_Model.objects.all(), widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Seleccione el modelo del dispositivo'
        }
      )
    )
  #         attrs={
  #           'placeholder': 'Seleccione el modelo del dispositivo'
  #         }
  #       ),
  #       'connection_type': Select(
  #         attrs={
  #           'placeholder': 'Seleccione el tipo de conexion del dispositivo'
  #         }
  #       ),
  #       'ip': TextInput(
  #         attrs={
  #           'placeholder': 'Si tuviera, ingrese direccion ip del dispositivo'
  #         }
  #       ),
  #       'dev_net_name': Select(
  #         attrs={
  #           'placeholder': 'Si tuviera, ingrese el nombre de regsitro en la red del dispositivo'
  #         }
  #       ),
  #       'dev_status': Select(
  #         attrs={
  #           'placeholder': 'Seleccione el estado funcional del dispositivo'
  #         }
  #       ),
  #       'serial_number': Select(
  #         attrs={
  #           'placeholder': 'Ingrese el número de serie'
  #         }
  #       ),
  #       'wall_port': Select(
  #         attrs={
  #           'placeholder': 'Seleccione el purto del que viene la conexión de red'
  #         }
  #       ),
  #       'employee': Select(
  #         attrs={
  #           'placeholder': 'Seleccione el empleado responsable del dispositivo'
  #         }
  #       )
  #     }

  # def save(self, commit=True):
  #   data={}
  #   form = super()
  #   try:
  #     if form.is_valid():
  #       form.save()
  #     else:
  #       data['error'] = form.errors.get_json_data()
  #   except Exception as e:
  #     data['error'] = str(e)
  #   return data
# class DeviceForm(ModelForm):

#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     for form in self.visible_fields():
#       form.field.widget.attrs['class'] = 'form-control m-1'
#     self.fields['dev_model'].widget.attrs['autofocus'] = True

#   class Meta:
#       model = Device
#       fields = '__all__'
#       widget = {
#         'dev_type': Select(
#           attrs={
#             'placeholder': 'Seleccione el tipo de dispositivo'
#           }
#         ),
#         'dev_model': Select(
#           attrs={
#             'placeholder': 'Seleccione el modelo del dispositivo'
#           }
#         ),
#         'connection_type': Select(
#           attrs={
#             'placeholder': 'Seleccione el tipo de conexion del dispositivo'
#           }
#         ),
#         'ip': TextInput(
#           attrs={
#             'placeholder': 'Si tuviera, ingrese direccion ip del dispositivo'
#           }
#         ),
#         'dev_net_name': Select(
#           attrs={
#             'placeholder': 'Si tuviera, ingrese el nombre de regsitro en la red del dispositivo'
#           }
#         ),
#         'dev_status': Select(
#           attrs={
#             'placeholder': 'Seleccione el estado funcional del dispositivo'
#           }
#         ),
#         'serial_number': Select(
#           attrs={
#             'placeholder': 'Ingrese el número de serie'
#           }
#         ),
#         'wall_port': Select(
#           attrs={
#             'placeholder': 'Seleccione el purto del que viene la conexión de red'
#           }
#         ),
#         'employee': Select(
#           attrs={
#             'placeholder': 'Seleccione el empleado responsable del dispositivo'
#           }
#         )
#       }

#   def save(self, commit=True):
#     data={}
#     form = super()
#     try:
#       if form.is_valid():
#         form.save()
#       else:
#         data['error'] = form.errors.get_json_data()
#     except Exception as e:
#       data['error'] = str(e)
#     return data

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

