from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Edifice, Location, Office_Loc, Province

class Office_Loc_Form(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    location=forms.ModelChoiceField(
        queryset=Location.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    class Meta:
        model = Office_Loc
        fields = [
            'province', 'location', 'edifice', 'floor', 'wing'
        ]
        widgets = {
            'edifice': Select(attrs={
                'class': 'form-control select2',
            }),
            'floor': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el Piso',
            }),
            'wing': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el Ala',
            }),
        }

        help_texts = {
            'floor': '* Ingrese el piso ingresando 2 numeros, ej. 01, y PB para Planta baja',
            'wing': '* En caso de no haber una desigancion del ala, se recomienda ingresar el nombre de la calle a la que mira la misma'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            if 'data' in kwargs:
                province_id = kwargs['data'].get('province')
                if province_id:
                    self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
                else:
                    self.fields['location'].queryset = Location.objects.none()

            if 'instance' in kwargs and kwargs['instance']:
                instance=kwargs['instance']

                if instance and instance.edifice and instance.edifice.location and instance.edifice.location.province:
                    self.fields['province'].queryset = Province.objects.all()
                    self.fields['province'].initial = instance.edifice.location.province.id

                    self.fields['location'].queryset = Location.objects.filter(province=instance.edifice.location.province)
                    self.fields['location'].initial = instance.edifice.location.id

                    self.fields['edifice'].queryset = Edifice.objects.filter(location=instance.edifice.location)
                    self.fields['edifice'].initial = instance.edifice.id

        def clean(self):
            cleaned_data = super().clean()

            edifice = self.cleaned_data.get('edifice')
            floor = self.cleaned_data.get('floor')
            wing = self.cleaned_data.get('wing')

            print("Edifice:", edifice)
            print("Floor:", floor)
            print("Wing:", wing)


            qs = Office_Loc.objects.all()

            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if edifice and floor and wing:
                if qs.filter(edifice=edifice, floor=floor, wing=wing).exists():
                    self.add_error('floor', f"Ya esta cargado el piso '{floor}' en el edificio {edifice}")
                    self.add_error('wing', f"Ya se encuentra registreada el ala: '{wing}', en el piso: '{floor}' del edificio {edifice}")
            return cleaned_data