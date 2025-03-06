from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Province
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc

class ProvinceModalForm(forms.ModelForm):

    class Meta:
        model = Province
        fields = '__all__'
        widgets = {
            'number_id': TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número correspondiente al Distrito (Ej: 04 para "CÓRDOBA" o 17 para "SALTA")',
                'autofocus': True,
                'id': 'id_modal_province_number'
            }),

            'province': TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': ' Ingrese el nombre del Distrito (Ej: "CÓRDOBA" o "SALTA")',
                'id': 'id_modal_province_input'
            })
        }
        help_texts = {
            'number_id': '* Ingrese los dos digitos identificatorios de la provincia, Ej: 04 para "CÓRDOBA" 0 17 para "SALTA"'
        }

class LocationModalForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'province': Select(
                attrs={
                'class': 'form-control select2',
                'id': 'id_modal_location_province_select'
            }),

            'location': TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la Localidad (Ej: "CÓRDOBA" o "SALTA")',
                'autofocus': True,
                'id': 'id_modal_location_input'
            })
        }

class EdificeModalForm(forms.ModelForm):

    class Meta:
        model = Edifice
        fields = '__all__'
        widgets = {
            'location': Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'id_modal_edifice_location_select'
                }),

            'edifice': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del Edificio (Ej: "CÓRDOBA" o "SALTA")',
                    'autofocus': True,
                    'id': 'id_modal_edifice_input'
                }),

            'address': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la dirección del Edificio (Ej: "Av Entre Ríos 1428, Barrio: Centro")',
                    'id': 'id_modal_edifice_address'
                })
        }

class DependencyModalForm(forms.ModelForm):
    class Meta:
        model = Dependency
        fields = '__all__'
        widgets = {
            'location': Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'id_modal_dependency_location_select'
                }),

            'dependency': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre de la Dependencia',
                    'autofocus': True,
                    'id': 'id_modal_dependency_input'
                }),

        }

class OfficeLocModalForm(forms.ModelForm):
    class Meta:
        model = Office_Loc
        fields = '__all__'
        widgets = {
            'edifice': Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'id_modal_loc_edifice_select'
                }),

            'floor': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el piso donde se encuentra la oficina',
                    'autofocus': True,
                    'id': 'id_modal_loc_floor_input'
                }),

            'wing': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el ala del edificio donde se encuentra la oficina',
                    'id': 'id_modal_loc_wing_input'
                })
        }
