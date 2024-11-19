from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import (
    Switch_Port, Brand, Dependency, Dev_Model, Dev_Type, Edifice, Location,
    Office, Office_Loc, Patchera, Province, Rack, Switch, Patch_Port
)

class SwitchPortForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    dependency = forms.ModelChoiceField(
        queryset=Dependency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    edifice = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    loc = forms.ModelChoiceField(
        queryset=Office_Loc.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    dev_type = forms.ModelChoiceField(
        queryset=Dev_Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    dev_model = forms.ModelChoiceField(
        queryset=Dev_Model.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    rack = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    patchera = forms.ModelChoiceField(
        queryset=Patchera.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    class Meta:
        model = Switch_Port
        fields = [
            'province', 'location', 'dependency', 'edifice', 'loc', 'office',
            'brand', 'dev_type', 'dev_model', 'rack', 'patchera', 'switch',
            'port_id', 'patch_port_out', 'patch_port_in', 'switch_in', 'switch_out', 'obs'
        ]
        widgets = {
            'switch': Select(attrs={'class': 'form-control select2'}),
            'port_id': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de puerto'}),
            'patch_port_out': Select(attrs={'class': 'form-control select2'}),
            'patch_port_in': Select(attrs={'class': 'form-control select2'}),
            'switch_in': Select(attrs={'class': 'form-control select2'}),
            'switch_out': Select(attrs={'class': 'form-control select2'}),
            'obs': Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese detalles particulares, si los hubiese'})
        }
        help_texts = {
            'patch_port_in': '* En caso de que la boca se alimente desde una patchera, seleccione el puerto aquí',
            'patch_port_out': '* En caso de que la boca alimente a una patchera, seleccione el puerto aquí',
            'switch_in': '* En caso de que la boca se alimente directamente desde un switch, selecciónelo aquí',
            'switch_out': '* En caso de que la boca vaya a un switch que distribuya la conexión, selecciónelo aquí'
        }

    def __init__(self, *args, **kwargs):
        super(SwitchPortForm, self).__init__(*args, **kwargs)

        # Inicializar querysets con todos los objetos
        self.fields['province'].queryset = Province.objects.all()
        self.fields['location'].queryset = Location.objects.all()
        self.fields['dependency'].queryset = Dependency.objects.all()
        self.fields['edifice'].queryset = Edifice.objects.all()
        self.fields['loc'].queryset = Office_Loc.objects.all()
        self.fields['office'].queryset = Office.objects.all()
        self.fields['brand'].queryset = Brand.objects.all()
        self.fields['dev_type'].queryset = Dev_Type.objects.all()
        self.fields['dev_model'].queryset = Dev_Model.objects.all()
        self.fields['rack'].queryset = Rack.objects.all()
        self.fields['patchera'].queryset = Patchera.objects.all()
        self.fields['switch'].queryset = Switch.objects.all()
        self.fields['patch_port_out'].queryset = Patch_Port.objects.all()
        self.fields['patch_port_in'].queryset = Patch_Port.objects.all()
        self.fields['switch_in'].queryset = Switch.objects.all()
        self.fields['switch_out'].queryset = Switch.objects.all()

        if self.instance.pk:
            # Manejo de instancia existente (edición)
            switch = self.instance.switch
            if switch:
                office = switch.office
                if office:
                    province = office.loc.edifice.location.province
                    location = office.loc.edifice.location
                    edifice = office.loc.edifice
                    loc = office.loc
                    dependency = office.dependency

                    self.initial['province'] = province
                    self.initial['location'] = location
                    self.initial['edifice'] = edifice
                    self.initial['loc'] = loc
                    self.initial['dependency'] = dependency
                    self.initial['office'] = office

                    self.fields['location'].queryset = Location.objects.filter(province=province)
                    self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
                    self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
                    self.fields['office'].queryset = Office.objects.filter(loc=loc)
                    self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location=location)

                dev_model = switch.dev_model
                if dev_model:
                    brand = dev_model.brand
                    dev_type = dev_model.dev_type
                    self.initial['brand'] = brand
                    self.initial['dev_type'] = dev_type
                    self.initial['dev_model'] = dev_model

                    self.fields['dev_model'].queryset = Dev_Model.objects.filter(
                        brand=brand,
                        dev_type=dev_type
                    )

                rack = switch.rack
                if rack:
                    self.initial['rack'] = rack
                    self.fields['patchera'].queryset = Patchera.objects.filter(rack=rack)
                    self.initial['patchera'] = self.instance.patchera if hasattr(self.instance, 'patchera') else None

                # Establecer valores iniciales para 'patch_port_out' y 'patch_port_in' si es necesario
                self.initial['patch_port_out'] = self.instance.patch_port_out
                self.initial['patch_port_in'] = self.instance.patch_port_in

                # Establecer valores iniciales para 'switch_in' y 'switch_out' si es necesario
                self.initial['switch_in'] = self.instance.switch_in
                self.initial['switch_out'] = self.instance.switch_out

            # Filtrar 'patch_port_out' y 'patch_port_in' basados en 'patchera'
            if self.initial.get('patchera'):
                self.fields['patch_port_out'].queryset = Patch_Port.objects.filter(patchera=self.initial['patchera'])
                self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera=self.initial['patchera'])

        else:
            # Manejo de nueva instancia (creación)
            # Obtener los valores seleccionados del formulario
            selected_province = self.data.get('province')
            selected_location = self.data.get('location')
            selected_dependency = self.data.get('dependency')
            selected_edifice = self.data.get('edifice')
            selected_loc = self.data.get('loc')
            selected_office = self.data.get('office')
            selected_brand = self.data.get('brand')
            selected_dev_type = self.data.get('dev_type')
            selected_rack = self.data.get('rack')
            selected_patchera = self.data.get('patchera')
            selected_switch = self.data.get('switch')

            # Convertir los valores a enteros si es posible
            def to_int(value):
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None

            selected_province = to_int(selected_province)
            selected_location = to_int(selected_location)
            selected_dependency = to_int(selected_dependency)
            selected_edifice = to_int(selected_edifice)
            selected_loc = to_int(selected_loc)
            selected_office = to_int(selected_office)
            selected_brand = to_int(selected_brand)
            selected_dev_type = to_int(selected_dev_type)
            selected_rack = to_int(selected_rack)
            selected_patchera = to_int(selected_patchera)
            selected_switch = to_int(selected_switch)

            # Filtrar los campos dependientes
            if selected_province:
                self.fields['location'].queryset = Location.objects.filter(province_id=selected_province)
                self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=selected_province)
                self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location__province_id=selected_province).distinct()
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=selected_province)
                self.fields['office'].queryset = Office.objects.filter(loc__edifice__location__province_id=selected_province)

            if selected_location:
                self.fields['edifice'].queryset = Edifice.objects.filter(location_id=selected_location)
                self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location_id=selected_location).distinct()
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=selected_location)
                self.fields['office'].queryset = Office.objects.filter(loc__edifice__location_id=selected_location)

            if selected_edifice:
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=selected_edifice)
                self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=selected_edifice)

            if selected_loc:
                self.fields['office'].queryset = Office.objects.filter(loc_id=selected_loc)

            if selected_dependency:
                self.fields['office'].queryset = self.fields['office'].queryset.filter(dependency_id=selected_dependency).distinct()

            if selected_brand or selected_dev_type:
                dev_model_filters = {}
                if selected_brand:
                    dev_model_filters['brand_id'] = selected_brand
                if selected_dev_type:
                    dev_model_filters['dev_type_id'] = selected_dev_type
                self.fields['dev_model'].queryset = Dev_Model.objects.filter(**dev_model_filters).distinct()

            if selected_rack:
                self.fields['patchera'].queryset = Patchera.objects.filter(rack_id=selected_rack)

            if selected_office or selected_rack:
                switch_filters = {}
                if selected_office:
                    switch_filters['office_id'] = selected_office
                if selected_rack:
                    switch_filters['rack_id'] = selected_rack
                self.fields['switch'].queryset = Switch.objects.filter(**switch_filters).distinct()

            if selected_patchera:
                self.fields['patch_port_out'].queryset = Patch_Port.objects.filter(patchera_id=selected_patchera)
                self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera_id=selected_patchera)

            if selected_switch:
                # Si necesitas filtrar otros campos basados en el switch seleccionado, agrégalos aquí
                pass

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
