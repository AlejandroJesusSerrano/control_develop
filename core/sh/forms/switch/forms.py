from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.patchera.models import Patchera
from core.sh.models.switch_port.models import Switch_Port
from core.sh.models.wall_port.models import Wall_Port

class SwitchForm(forms.ModelForm):
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

    patchera_ports = forms.ModelChoiceField(
        queryset = Patchera.objects.all(),
        widget = forms.Select(attrs={
            'class': 'form-control select2', 
            'id': 'id_patchera_ports',
            'order_by': 'rack'}),
        required = False
    )

    switch_ports = forms.ModelChoiceField(
        queryset = Switch.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_ports'}),
        required = False
    )

    # Otros campos existentes
    brand = forms.ModelChoiceField(
        queryset = Brand.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_brand'}),
        required = False
    )

    model = forms.ModelChoiceField(
        queryset = Dev_Model.objects.filter(dev_type__dev_type='SWITCH'),
        widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dev_model'}),
        required = False
    )

    class Meta:
        model = Switch
        fields = [
            'brand', 'model', 'serial_n', 'ports_q', 'rack', 'province', 'location', 'dependency', 'edifice', 'edifice_ports', 'loc', 'loc_ports', 'office', 'office_ports', 'rack_ports', 'switch_rack_pos', 'wall_port_in', 'switch_ports', 'switch_port_in', 'patchera_ports', 'patch_port_in', 'ip'
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
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección IP del Switch',
                'id': 'id_ip_input'
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

            if 'brand' in self.data:
                try:
                    brand_id = int(self.data.get('brand'))
                    self.fields['model'].queryset = Dev_Model.objects.filter(
                        dev_type__dev_type='SWITCH',
                        brand_id=brand_id
                        )
                except (ValueError, TypeError):
                    pass

            if 'data' in kwargs:
                location_id = kwargs['data'].get('location')
                if location_id:
                    try:
                        location = Location.objects.get(id=location_id)
                        self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=location).order_by('edifice')
                        self.fields['loc_ports'].queryset = Office_Loc.objects.filter(edifice__location=location).order_by('office_location')
                        self.fields['office_ports'].queryset = Office.objects.filter(loc__edifice__location=location).order_by('office')
                        self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice__location=location).order_by('rack')
                        self.fields['rack_ports'].queryset = Rack.objects.filter(office__loc__edifice__location=location).order_by('rack')
                        self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office__loc__edifice__location=location).order_by('wall_port')
                        self.fields['patchera_ports'].queryset = Patchera.objects.filter(rack__office__loc__edifice__location=location).order_by('rack')
                        self.fields['switch_ports'].queryset = Switch.objects.filter(office__loc__edifice__location=location).order_by('model')
                        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__rack__office__loc__edifice__location=location).order_by('port_id')
                        self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera__rack__office__loc__edifice__location=location).order_by('port')

                    except Location.DoesNotExist:

                        self.fields['edifice_ports'].queryset = Edifice.objects.all()
                        self.fields['loc_ports'].queryset = Office_Loc.objects.all()
                        self.fields['office_ports'].queryset = Office.objects.all()
                        self.fields['rack'].queryset = Rack.objects.all()
                        self.fields['rack_ports'].queryset = Rack.objects.all()
                        self.fields['wall_port_in'].queryset = Wall_Port.objects.all()
                        self.fields['patchera_ports'].queryset = Patchera.objects.all()
                        self.fields['switch_ports'].queryset = Switch.objects.all()
                        self.fields['switch_port_in'].queryset = Switch_Port.objects.all()
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

                        self.fields['dependency'].queryset = Dependency.objects.filter(location=instance.office.dependency.location)
                        self.fields['dependency'].initial = instance.office.dependency.id

                        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=instance.office.loc.edifice)
                        self.fields['loc'].initial = instance.office.loc.id

                        self.fields['office'].queryset = Office.objects.filter(loc=instance.office.loc, dependency=instance.office.dependency)
                        self.fields['office'].initial = instance.office.id

                        self.fields['rack'].queryset = Rack.objects.filter(office=instance.office)
                        self.fields['rack'].initial = instance.rack

                        self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office=instance.office)
                        self.fields['wall_port_in'].initial = instance.wall_port_in

                        self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch=instance)
                        self.fields['switch_port_in'].initial = instance.switch_port_in

                self.fields['office'].required = False

        def clean(self):
            cleaned_data = super().clean()
            brand = cleaned_data.get('brand')
            model = cleaned_data.get('model')
            serial_n = cleaned_data.get('serial_n')
            rack = cleaned_data.get('rack')
            switch_rack_pos = cleaned_data.get('switch_rack_pos')
            office = cleaned_data.get('office')

            if not office and not rack:
                self.add_error('office', 'Debe seleccionar una oficina o un rack.')
                self.add_error('rack', 'Debe seleccionar una oficina o un rack.')
            elif rack and not office:
                cleaned_data['office'] = rack.office

            if brand and model:
                if model.brand != brand:
                    self.add_error('model', f'El modelo {model} no corresponde a la marca {brand}')

            qs = Switch.objects.all()
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.filter(model=model, serial_n=serial_n).exists():
                self.add_error('model', f'Ya se encuentra registrado el switch {model} con el S/N° {serial_n}.')
                self.add_error('serial_n', f'El S/N° {serial_n}, ya se ecuentra registrado para el switch {model}.')

            if rack and switch_rack_pos:
                if qs.filter(rack=rack, switch_rack_pos=switch_rack_pos).exists():
                    self.add_error('rack', f'ya se encuentra ocupáda la posicion {switch_rack_pos} en el rack {rack}')
                    self.add_error('switch_rack_pos', f'el rack {rack}, ya tiene ocupada la posicion de switch {switch_rack_pos}')
            return cleaned_data
