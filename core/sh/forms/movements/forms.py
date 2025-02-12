# core/sh/forms/movements/forms.py
from django import forms
from django.forms import ModelForm, Select, Textarea, DateInput
from core.sh.models.connection_type.models import Connection_Type
from core.sh.models.movements.models import Movements
from core.sh.models.device.models import Device
from core.sh.models.switch.models import Switch
from core.sh.models.move_type.models import Move_Type
from core.sh.models.tehcs.models import Techs
from core.sh.models.suply.models import Suply
from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_type.models import Dev_Type
from core.sh.models.edifice.models import Edifice
from core.sh.models.employee.models import Employee
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack

class MovementsForm(ModelForm):
    # Campos extras para filtrar (no pertenecen al modelo Movements)
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
        required=False
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_location'}),
        required=False
    )
    dependency = forms.ModelChoiceField(
        queryset=Dependency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
        required=False
    )
    edifice = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
        required=False
    )
    loc = forms.ModelChoiceField(
        queryset=Office_Loc.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
        required=False
    )

    # Estos dos sí pertenecen al modelo Movements
    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_office'}),
        required=False  # o True si deseas que sea obligatorio
    )
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_employee'}),
        required=False
    )

    # Filtrado de Dev_Type (lo usas sólo para filtrar?)
    dev_type = forms.ModelChoiceField(
        queryset=Dev_Type.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'id': 'id_dev_type',
            'data-preselected': ''
            }),
        required=False
    )

    d_brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'id': 'id_d_brand',
            'data-preselected': ''
            }),
        required=False
    )

    s_brand = forms.ModelChoiceField(
        Brand.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_s_brand'}),
        required=False
    )

    rack = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack'}),
        required=False
    )

    # Campos "ChoiceField" para serial_n, ip, etc.
    # Por ej. Switch Serial
    s_serial_n = Switch.objects.values_list('serial_n', flat=True).distinct()
    s_serial_n_choices = [('', '----------')] + [(serial_n, serial_n) for serial_n in s_serial_n]

    switch_serial_n = forms.ChoiceField(
        choices=s_serial_n_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_serial_n'}),
        required=False
    )

    # Device Serial
    d_serial_n = Device.objects.values_list('serial_n', flat=True).distinct()
    d_serial_n_choices = [('', '----------')] + [(serial_n, serial_n) for serial_n in d_serial_n]

    device_serial_n = forms.ChoiceField(
        choices=d_serial_n_choices,
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'id': 'id_device_serial_n',
            'data-preselected': ''
            }),
        required=False
    )

    # Switch Rack Pos
    s_rack_pos = Switch.objects.values_list('switch_rack_pos', flat=True).distinct()
    s_rack_pos_choices = [('', '----------')] + [(pos, pos) for pos in s_rack_pos if pos]

    switch_rack_pos = forms.ChoiceField(
        choices=s_rack_pos_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_rack_pos'}),
        required=False
    )

    # IP de Device
    d_ips = Device.objects.values_list('ip', flat=True).distinct()
    d_ip_choices = [('', '----------')] + [(ip, ip) for ip in d_ips if ip]

    d_ip = forms.ChoiceField(
        choices=d_ip_choices,
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'id': 'd_id_ip',
            'data-preselected': ''
            }),
        required=False
    )

    s_ips = Switch.objects.values_list('ip', flat=True).distinct()
    s_ip_choices = [('', '----------')] + [(ip, ip) for ip in s_ips if ip]

    s_ip = forms.ChoiceField(
        choices=s_ip_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 's_id_ip'}),
        required=False
    )

    class Meta:
        model = Movements
        fields = [
            'office', 'employee', 'device', 'switch', 'move', 'techs', 'date', 'suply', 'detail', 'dev_type', 'd_brand', 'rack', 'switch_serial_n', 'switch_rack_pos', 'device_serial_n', 'd_ip', 's_brand', 'province', 'location', 'dependency', 'edifice', 'loc', 's_ip'
        ]

        widgets = {
            'device': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_device',
                'data-preselected': ''
                }),
            'switch': Select(attrs={'class': 'form-control select2', 'id': 'id_switch'}),
            'move': Select(attrs={'class': 'form-control select2', 'id': 'id_move'}),
            'techs': Select(attrs={'class': 'form-control select2', 'id': 'id_techs'}),
            'date': DateInput(attrs={
                'class': 'form-control datepicker',
                'id': 'id_date',
                'autocomplete': 'off',
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy'
            }),
            'suply': Select(attrs={'class': 'form-control select2', 'id': 'id_suply'}),
            'detail': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalle del movimiento...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['dev_type'].widget.attrs['data-preselected'] = str(self.instance.dev_type.pk)

            if self.instance:
                if self.instance.dev_type:
                    self.fields['dev_type'].widget.attrs['data-preselected'] = str(self.instance.dev_type.pk)
                if self.instance.brand:
                    self.fields['d_brand'].widget.attrs['data-preselected'] = str(self.instance.brand.pk)
                if self.instance.device:
                    self.fields['device'].widget.attrs['data-preselected'] = str(self.instance.device.pk)

        elif 'initial' in kwargs:
            initial = kwargs['initial']
            if 'dev_type' in initial:
                self.fields['dev_type'].widget.attrs['data-preselected'] = initial['dev_type']
            if 'd_brand' in initial:
                self.fields['d_brand'].widget.attrs['data-preselected'] = initial['d_brand']
            if 'device' in initial:
                self.fields['device'].widget.attrs['data-preselected'] = initial['device']