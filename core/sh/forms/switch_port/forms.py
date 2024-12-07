from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.dev_type.models import Dev_Type
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patchera.models import Patchera
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.switch_port.models import Switch_Port


class SwitchPortForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset = Province.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    dependency = forms.ModelChoiceField(
        queryset = Dependency.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    edifice = forms.ModelChoiceField(
        queryset = Edifice.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    loc = forms.ModelChoiceField(
        queryset = Office_Loc.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    office = forms.ModelChoiceField(
        queryset = Office.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    brand = forms.ModelChoiceField(
        queryset = Brand.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    dev_type = forms.ModelChoiceField(
        queryset = Dev_Type.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    dev_model = forms.ModelChoiceField(
        queryset = Dev_Model.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    rack = forms.ModelChoiceField(
        queryset = Rack.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    patchera = forms.ModelChoiceField(
        queryset = Patchera.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control select2'}),
        required = False
    )

    class Meta:
        model = Switch_Port
        fields = [
            'province', 'location', 'dependency', 'edifice', 'loc', 'office',
            'brand', 'dev_type', 'dev_model', 'rack', 'patchera', 'switch',
            'port_id', 'obs'
        ]
        widgets = {
            'switch': Select(attrs={'class': 'form-control select2'}),
            'port_id': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de puerto'}),
            'obs': Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese detalles particulares, si los hubiese'})
        }

    def __init__(self, *args, **kwargs):
        super(SwitchPortForm, self).__init__(*args, **kwargs)

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

        if self.instance.pk:
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

                dev_model = switch.model
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

        else:
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

            if selected_switch:
                pass

    def clean(self):
        cleaned_data = super().clean()
        switch = cleaned_data.get('switch')
        port_id = cleaned_data.get('port_id')

        if Switch_Port.objects.filter(switch=switch, port_id=port_id).exists():
            self.add_error('switch', f"Ya existe un puerto '{port_id}' en el switch seleccionado.")
            self.add_error('port_id', f"El puerto '{port_id}' ya está registrado para el switch especificado.")

        return cleaned_data
