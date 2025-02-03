# movements/forms.py
from django import forms
from django.forms import ModelForm, Select, Textarea, DateInput
from core.sh.models import Movements, Device, Switch, Move_Type, Techs, Suply
from core.sh.models.office.models import Office

class MovementsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuración inicial de querysets
        self.fields['device'].queryset = Device.objects.none()
        self.fields['switch'].queryset = Switch.objects.none()

        # Si estamos editando una instancia existente
        if self.instance.pk:
            if self.instance.device:
                self.fields['device'].queryset = Device.objects.filter(pk=self.instance.device.pk)
                self.fields['switch'].queryset = Switch.objects.filter(office=self.instance.device.office)
            elif self.instance.switch:
                self.fields['switch'].queryset = Switch.objects.filter(pk=self.instance.switch.pk)
                self.fields['device'].queryset = Device.objects.filter(office=self.instance.switch.office)

    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=Select(attrs={
            'class': 'form-control select2',
            'id': 'id_office',
            'data-url': '/get_devices_and_switches/'
        }),
        required=False,
        label="Oficina"
    )

    class Meta:
        model = Movements
        fields = '__all__'
        widgets = {
            'device': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_device',
                'disabled': True
            }),
            'switch': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_switch',
                'disabled': True
            }),
            'move': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_move_type'
            }),
            'techs': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_techs'
            }),
            'date': DateInput(attrs={
                'class': 'form-control datepicker',
                'id': 'id_date',
                'autocomplete': 'off',
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy'
            }),
            'suply': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_suply'
            }),
            'detail': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalle del movimiento...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        device = cleaned_data.get('device')
        switch = cleaned_data.get('switch')
        move_type = cleaned_data.get('move')

        # Validación de campos requeridos según tipo de movimiento
        if move_type.requires_device and not device:
            self.add_error('device', 'Este tipo de movimiento requiere un dispositivo')
        if move_type.requires_switch and not switch:
            self.add_error('switch', 'Este tipo de movimiento requiere un switch')
        return cleaned_data

# from django.forms import *
# from django.forms import ModelForm, Select, Textarea, DateInput

# from core.sh.models.movements.models import Movements


# class MovementsForm(ModelForm):

#   class Meta:
#       model = Movements
#       fields = '__all__'
#       widget = {
#         'device': Select(
#           attrs={
#             'class': 'form-control select2',
#             'id': 'id_device'
#           }
#         ),

#         'switch': Select(
#           attrs={
#             'class': 'form-control select2'
#           }
#         ),

#         'port_id': Select(
#           attrs={
#             'placeholder': 'Seleccione el tipo de movimiento',
#             'id': 'id_port_id_input'
#           }
#         ),
#         'techs': Select(
#           attrs={
#             'placeholder': 'Seleccione el Técnico responsable del movimiento',
#             'id': 'id_techs'
#           }
#         ),
#         'date': DateInput(
#           attrs={
#             'placeholder': 'Ingrese la fecha del movimiento',
#             'id': 'id_move_date_input'
#           }
#         ),
#         'suply': Select(
#           attrs={
#             'placeholder': 'En caso de haberse requerido, ingrese el insumo utilizado',
#             'id': 'id_suply'
#           }
#         ),
#         'detail': Textarea(
#           attrs={
#             'placeholder': 'Describa el detalle del movimiento realizado',
#             'id': 'id_detail_move_input'
#           }
#         ),
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

