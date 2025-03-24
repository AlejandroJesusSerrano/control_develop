from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Dependency, Device, Office, Brand, Dev_Type, Employee, Switch_Port, Dev_Model, Wall_Port
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch

class DeviceForm(forms.ModelForm):

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

    edifice_ports = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice_ports'}),
        required=False
    )

    loc_ports = forms.ModelChoiceField(
        queryset=Office_Loc.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc_ports'}),
        required=False
    )

    office_ports = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_office_ports'}),
        required=False
    )

    rack_ports = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack_ports'}),
        required=False
    )

    switch_ports = forms.ModelChoiceField(
        queryset=Switch.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_ports'}),
        required=False
    )

    patchera_ports = forms.ModelChoiceField(
        queryset=Patchera.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_patchera_ports'}),
        required=False
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.exclude(models_brand__dev_type__dev_type='SWITCH').distinct(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_brand'}),
        required=False
    )

    dev_type = forms.ModelChoiceField(
        queryset=Dev_Type.objects.exclude(dev_type='SWITCH'),
        widget=forms.Select(attrs={'class':'form-control select2', 'id': 'id_dev_type'}),
        required=False
    )

    dev_model = forms.ModelChoiceField(
        queryset=Dev_Model.objects.exclude(dev_type__dev_type='SWITCH'),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dev_model'}),
        required=True
    )

    class Meta:
        model = Device
        fields = [
            'province', 'location', 'dependency', 'edifice', 'loc', 'dev_model', 'connection', 'ip', 'net_name', 'dev_status', 'serial_n', 'office', 'edifice_ports', 'loc_ports', 'office_ports', 'rack_ports', 'switch_ports', 'wall_port_in', 'switch_port_in', 'patchera_ports', 'patch_port_in', 'employee'
        ]
        widgets = {
            'connection': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_connection'
            }),
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección ip',
                'id': 'id_ip_input'
            }),
            'net_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de registro en la red',
                'id': 'id_net_name_input'
            }),
            'dev_status': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_dev_status'
            }),
            'serial_n': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de serie',
                'id': 'id_serial_n_input'
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
            }),
            'employee': SelectMultiple(attrs={
                'class': 'form-control select2',
                'id': 'id_employee'}),
        }

        help_texts = {
            'ip': 'Solo en caso de tener una dirección IP asignada.',
            'net_name': 'Solo en caso de tener un nombre de registro en la red.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'data' in kwargs:
            location_id = kwargs['data'].get('location')
            if location_id:
                try:
                    location = Location.objects.get(id=location_id)
                    self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=location).order_by('edifice')
                    self.fields['loc_ports'].queryset = Office_Loc.objects.filter(edifice__location=location).order_by('office_location')
                    self.fields['office_ports'].queryset = Office.objects.filter(loc__edifice__location=location).order_by('office')
                    self.fields['rack_ports'].queryset = Rack.objects.filter(office__loc__edifice__location=location).order_by('rack')
                    self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office__loc__edifice__location=location).order_by('wall_port')
                    self.fields['switch_ports'].queryset = Switch.objects.filter(office__loc__edifice__location=location).order_by('model')
                    self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__rack__office__loc__edifice__location=location).order_by('port_id')
                    self.fields['patchera_ports'].queryset = Patchera.objects.filter(rack__office__loc__edifice__location=location).order_by('patchera')
                    self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera__rack__office__loc__edifice__location=location).order_by('port')

                except (Location.DoesNotExist, ValueError):

                    self.fields['edifice_ports'].queryset = Edifice.objects.all()
                    self.fields['loc_ports'].queryset = Office_Loc.objects.all()
                    self.fields['office_ports'].queryset = Office.objects.all()
                    self.fields['rack_ports'].queryset = Rack.objects.all()
                    self.fields['wall_port_in'].queryset = Wall_Port.objects.all()
                    self.fields['switch_ports'].queryset = Switch.objects.all()
                    self.fields['switch_port_in'].queryset = Switch_Port.objects.all()
                    self.fields['patchera_ports'].queryset = Patchera.objects.all()
                    self.fields['patch_port_in'].queryset = Patch_Port.objects.all()
            else:
                self.fields['edifice_ports'].queryset = Edifice.objects.all()

        if 'instance' in kwargs and kwargs['instance']:
            instance=kwargs['instance']
            if instance.office and instance.office.loc and instance.office.loc.edifice and instance.office.loc.edifice.location and instance.office.loc.edifice.location.province and instance.office.dependency:
                self.fields['province'].queryset = Province.objects.all()
                self.fields['province'].initial = instance.office.loc.edifice.location.province.id

                self.fields['location'].queryset = Location.objects.filter(province=instance.office.loc.edifice.location.province)
                self.fields['location'].initial = instance.office.loc.edifice.location.id

                self.fields['edifice'].queryset = Edifice.objects.filter(location=instance.office.loc.edifice.location)
                self.fields['edifice'].initial = instance.office.loc.edifice.id

                self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=instance.office.loc.edifice.location)
                self.fields['edifice_ports'].initial = instance.office.loc.edifice.id

                self.fields['dependency'].queryset = Dependency.objects.filter(location=instance.office.loc.edifice.location)
                self.fields['dependency'].initial = instance.office.dependency.id

                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=instance.office.loc.edifice)
                self.fields['loc'].initial = instance.office.loc.id

                self.fields['office'].queryset = Office.objects.filter(loc=instance.office.loc, dependency=instance.office.dependency)
                self.fields['office'].initial = instance.office.id

                self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office=instance.office)
                if instance.wall_port_in:
                    self.fields['wall_port_in'].initial = instance.wall_port_in.id

                self.fields['employee'].queryset = Employee.objects.filter(office=instance.office)

                self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__office=instance.office)
                self.fields['switch_port_in'].initial = instance.switch_port_in.id if self.instance.switch_port_in else None


        self.fields['office'].required = True

    def clean(self):
        cleaned_data = super().clean()

        dev_model = cleaned_data.get('dev_model')
        ip = cleaned_data.get('ip')
        net_name = cleaned_data.get('net_name')
        serial_n = cleaned_data.get('serial_n')

        qs = Device.objects.all()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.filter(dev_model=dev_model, serial_n=serial_n).exists():
            self.add_error('serial_n', f'Ya existe el dispositivo {dev_model} con el número de serie: {serial_n}.')
            self.add_error('dev_model', f'Ya se encuentra asignado el número de serie: {serial_n}, para el dispositivo {dev_model}.')

        if ip and qs.filter(ip=ip).exists():
            self.add_error('ip', f'la dirección IP: {ip}. Ya de encutra asignada a otro dispositivo.')

        if net_name and qs.filter(net_name=net_name).exists():
            self.add_error('net_name', f'El nombre de registro en la red: {net_name}. Ya se encuentra asignado a otro dispositivo.')

        return cleaned_data