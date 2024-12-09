from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
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
            'province', 'location', 'dependency', 'edifice', 'loc', 'office', 'rack', 'patchera', 'switch', 'port_id', 'obs'
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
        self.fields['rack'].queryset = Rack.objects.all()
        self.fields['patchera'].queryset = Patchera.objects.all()
        self.fields['switch'].queryset = Switch.objects.all()

        if self.instance.pk:

            if self.instance.switch.office and self.instance.switch.office.loc and self.instance.switch.office.loc.edifice and self.instance.switch.office.loc.edifice.location and self.instance.switch.office.loc.edifice.location.province and self.instance.switch.office.dependency and self.instance.switch.office.dependency.location:

                province = self.instance.switch.office.loc.edifice.location.province
                dependency = self.instance.switch.office.dependency
                location = self.instance.switch.office.loc.edifice.location
                edifice = self.instance.switch.office.loc.edifice
                loc = self.instance.switch.office.loc
                office = self.instance.switch.office
                rack = self.instance.switch.rack
                if self.instance.switch and self.instance.switch.patch_port_in and self.instance.switch.patch_port_in.patchera:
                    patchera = self.instance.switch.patch_port_in.patchera
                switch = self.instance.switch

                self.initial['province'] = province.id
                self.initial['location'] = location.id
                self.initial['dependency'] = dependency.id
                self.initial['edifice'] = edifice.id
                self.initial['loc'] = loc.id
                self.initial['office'] = self.instance.switch.office.id
                self.initial['rack'] = self.instance.switch.rack.id
                self.initial['patchera'] = self.instance.switch.patch_port_in

                self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
                self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.switch.office.loc.edifice.location).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.switch.office.dependency.location).order_by('dependency')
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.switch.office.loc.edifice).order_by('office_location')
                self.fields['office'].queryset = Office.objects.filter(loc=self.instance.switch.office.loc, dependency=self.instance.switch.office.dependency).order_by('office')

                if 'province' in self.data:
                    try:
                        province_id = int(self.data.get('province'))
                        self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
                        self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
                        self.fields['dependency'].queryet = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
                        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location__province_id=province_id).order_by('office_location')
                        self.fields['office'].queryset = Office.objects.filter(
                            loc__edifice__location__province_id=province_id,
                            dependency__location__province_id=province_id
                            ).order_by('office')
                        self.fields['rack'].queryset = Rack.objects.filter(
                            office__loc__edifice__location__province_id=province_id,
                            office__dependency__location__province_id=province_id
                            ).order_by('rack')
                        self.fields['patchera'].queryset = Patchera.objects.filter(
                            rack__office__loc__edifice__location__province_id=province_id,
                            rack__office__dependency__location__province_id=province_id
                        ).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(
                            office__loc__edifice__location__province_id=province_id,
                            office__dependency__location__province_id=province_id
                        ).order_by('switch')
                        if 'rack' in self.data:
                            self.fields['switch'].queryset = Switch.objects.filter(
                                rack__office__loc__edifice__location__province_id=province_id,
                                rack__office__dependency__location__province_id=province_id
                            ).order_by('switch')
                        elif 'patchera' in self.data:
                            self.fields['patchera'].queryset = Switch.objects.filter(
                                patchera__rack__office__loc__edifice__location__province_id=province_id,
                                patchera__rack__office__dependency__location__province_id=province_id
                            ).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['location'].queryset = self.instance.switch.office.loc.edifice.location.province.location_set.order_by('location')

                if 'location' in self.data:
                    try:
                        location_id = int(self.data.get('location'))
                        self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
                        self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id).order_by('dependency')
                        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice__location_id=location_id).order_by('office_location')
                        self.fields['office'].queryset = Office.objects.filter(
                            loc__edifice__location_id=location_id,
                            dependency__location_id=location_id
                            ).order_by('office')
                        self.fields['rack'].queryset = Rack.objects.filter(
                            office__loc__edifice__location_id=location_id,
                            office__dependency__location_id=location_id
                            ).order_by('rack')
                        self.fields['patchera'].queryset = Patchera.objects.filter(
                            rack__office__loc__edifice__location_id=location_id,
                            rack__office__dependency__location_id=location_id
                        ).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(
                            office__loc__edifice__location_id=location_id,
                            office__dependency__location_id=location_id
                        ).order_by('switch')
                        if 'rack' in self.data:
                            self.fields['switch'].queryset = Switch.objects.filter(
                                rack__office__loc__edifice__location_id=location_id,
                                rack__office__dependency__location_id=location_id
                            ).order_by('switch')
                        elif 'patchera' in self.data:
                            self.fields['patchera'].queryset = Switch.objects.filter(
                                patchera__rack__office__loc__edifice__location_id=location_id,
                                patchera__rack__office__dependency__location_id=location_id
                            ).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['edifice'].queryset = self.instance.switch.office.loc.edifice.location.edifice_location.order_by('edifice')
                    self.fields['dependency'].queryset = self.instance.switch.office.dependency.location.dependency_location.order_by('dependency')

                if 'dependency' in self.data:
                    try:
                        dependency_id = int(self.data.get('dependency'))
                        self.fields['office'].queryset = Office.objects.filter(dependency_id=dependency_id).order_by('office')
                        self.fields['rack'].queryset = Rack.objects.filter(
                            office__dependency__location_id=location_id
                        ).order_by('rack')
                        self.fields['patchera'].queryset = Patchera.objects.filter(
                            rack__office__dependency__location_id=location_id
                        ).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(
                            office__dependency__location_id=location_id
                        ).order_by('switch')
                        if 'rack' in self.data:
                            self.fields['switch'].queryset = Switch.objects.filter(
                                rack__office__dependency__location_id=location_id
                            ).order_by('switch')
                        elif 'patchera' in self.data:
                            self.fields['patchera'].queryset = Switch.objects.filter(
                                patchera__rack__office__dependency__location_id=location_id
                            ).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['office'].queryset = self.instance.switch.office.dependency.offices_dependencies.order_by('office')

                if 'edifice' in self.data:
                    try:
                        edifice_id = int(self.data.get('edifice'))
                        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice_id).order_by('office_location')
                        self.fields['office'].queryset = Office.objects.filter(loc__edifice_id=edifice_id).order_by('office')
                        self.fields['rack'].queryset = Rack.objects.filter(office__loc__edifice_id=edifice_id).order_by('rack')
                        self.fields['patchera'].queryset = Patchera.objects.filter(rack__loc__edifice_id=edifice_id).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(office__loc__edifice_id=edifice_id).order_by('switch')
                        if 'rack' in self.data:
                            self.fields['switch'].queryset = Switch.objects.filter(rack__office__loc__edifice_id=edifice_id).order_by('switch')
                        elif 'patchera' in self.data:
                            self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office__loc__edifice_id=edifice_id).order_by('switch')

                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['loc'].queryset = self.instance.switch.office.loc.edifice.office_loc_edifice.order_by('office_location')

                if 'loc' in self.data:
                    try:
                        loc_id = int(self.data.get('loc'))
                        self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id).order_by('office')
                        self.fields['rack'].queryset = Rack.objects.filter(office__loc_id=loc_id).order_by('rack')
                        self.fields['patchera'].queryset = Patchera.objects.filter(rack__office__loc_id=loc_id).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(office__loc_id=loc_id).order_by('switch')
                        if 'rack' in self.data:
                            self.fields['switch'].queryset = Switch.objects.filter(rack__office__loc_id=loc_id).order_by('switch')
                        elif 'patchera' in self.data:
                            self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office__loc_id=loc_id).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['office'].queryset = self.instance.switch.office.loc.office_location.order_by('office')

                if 'office' in self.data:
                    try:
                        office_id = int(self.data.get('office'))
                        self.fields['rack'].queryset = Rack.objects.filter(office_id=office_id).order_by('rack')
                        self.fields['patchera'].queryset = Patchera.objects.filter(rack__office_id=office_id).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(office_id=office_id).order_by('switch')
                        if 'rack' in self.data:
                            self.fields['switch'].queryset = Switch.objects.filter(rack__office_id=office_id).order_by('switch')
                        elif 'patchera' in self.data:
                            self.fields['patchera'].queryset = Switch.objects.filter(patchera__rack__office_id=office_id).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    self.fields['rack'].queryset = self.instance.switch.rack.office.rack_office.order_by('rack')

                if 'rack' in self.data:
                    try:
                        rack_id = int(self.data.get(rack))
                        self.fields['patchera'].queryset = Patchera.objects.filter(rack_id=rack_id).order_by('patchera')
                        self.fields['switch'].queryset = Switch.objects.filter(
                            patchera__rack_id=rack_id,
                            rack_id=rack_id).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    if self.instance.switch and self.instance.switch.patch_port_in and self.instance.switch.patch_port_in.patchera:
                        patchera=self.instance.switch.patch_port_in.patchera
                        self.fields['patchera'].queryset = self.instance.switch.patch_port_in.patchera.rack.patchera_rack.order_by('patchera')
                    else:
                        self.fields['patchera'].queryset = Patchera.objects.none()

                if 'patchera' in self.data:
                    try:
                        patchera_id = int(self.data.get(patchera))
                        self.fields['switch'].queryset = Switch.objects.filter(patchera_id=patchera_id).order_by('switch')
                    except (ValueError, TypeError):
                        pass
                elif self.instance.pk:
                    if self.instance.switch and self.instance.switch.patch_port_in and self.instance.switch.patch_port_in.patchera:
                        patch_port_in=self.instance.switch.patch_port_in
                        self.fields['switch'].queryset = self.instance.switch.patch_port_in.switch_patch_port_in.order_by('switch')
                    else:
                        self.fields['patch_port_in'].queryset = Patch_Port.objects.none()

                if office or rack:
                    switch_filters = {}
                    if office:
                        switch_filters['office_id'] = office
                    if rack:
                        switch_filters['rack_id'] = rack
                    self.fields['switch'].queryset = Switch.objects.filter(**switch_filters).distinct()

                if switch:
                    pass

    def clean(self):
        cleaned_data = super().clean()
        switch = cleaned_data.get('switch')
        port_id = cleaned_data.get('port_id')

        if Switch_Port.objects.filter(switch=switch, port_id=port_id).exists():
            self.add_error('switch', f"Ya existe un puerto '{port_id}' en el switch seleccionado.")
            self.add_error('port_id', f"El puerto '{port_id}' ya está registrado para el switch especificado.")

        return cleaned_data
