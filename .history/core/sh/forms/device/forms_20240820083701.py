from django import forms
from django.forms import Form, ModelChoiceField, Select

from core.sh.models import Brand, Connection_Type, Dev_Model, Dev_Status, Dev_Type, Employee, Office, Switch_Port, Wall_Port


class DeviceForm(Form):

    dev_type = ModelChoiceField(
      queryset = Dev_Type.objects.all(),
      widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Seleccione el tipo de dispositivo'
        }
      )
    )

    brand = ModelChoiceField(
      queryset = Brand.objects.all(),
      widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Selecciona la Marca'
        }
      )
    )

    dev_model = ModelChoiceField(
      queryset = Dev_Model.objects.none(),
      widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Seleccione el modelo del dispositivo'
        }
      )
    )

    connection_type = ModelChoiceField(
      queryset = Connection_Type.objects.all(),
      widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Seleccione el tipo de conexion del dispositivo'
        }
      )
    )

    ip = forms.CharField(
      widget = forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Si tuviera, ingrese la dirección ip del dispositivo'
          }
        )
    )

    dev_net_name = forms.CharField(
      widget = forms.TextInput(
        attrs = {
          'class': 'form-control',
          'placeholder': 'Si tuviera, ingrese el nombre de regsitro en la red del dispositivo'
        }
      )
    )

    dev_status = ModelChoiceField(
      queryset = Dev_Status.objects.all(),
      widget = Select(
        attrs = {
        'class': 'form-control select2',
        'placeholder': 'Seleccione el estado funcional del dispositivo'
        }
      )
    )

    serial_number = forms.CharField(
      widget = forms.TextInput(
        attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el número de serie'
        }
      )
    )

    office =  ModelChoiceField(
      queryset = Office.objects.all(),
      widget = Select(
        attrs= {
          'class': 'form-control select2',
          'placeholder': 'Selecciona la oficina'
        }
      )
    )

    wall_port = ModelChoiceField(
      queryset = Wall_Port.objects.none(),
      widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Seleccione el puerto del que viene la conexión de red'
        }
      )
    ),

    switch_port = ModelChoiceField(
      queryset = Switch_Port.objects.none(),
      widget = Select(
        attrs = {
          'class': 'form-control select2',
          'placeholder': 'Seleccione el puerto del Switch'
        }
      )
    ),

    employee = ModelChoiceField(
      queryset = Employee.objects.none(),
      widget = Select(
        attrs={
          'class': 'form-control select2',
          'placeholder': 'Seleccione el empleado responsable del dispositivo'
        }
      )
    )