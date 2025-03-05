from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Location

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('province', 'location')
        widgets = {
        'province': Select(
            attrs={
                'class': 'form-control select2',
                'id': 'id_province',
                'autofocus': True
            }
        ),

        'location': TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una localidad',
                'id': 'id_location_input'
            }
        )
    }

    def clean(self):
        cleaned_data=super().clean()

        province = self.cleaned_data.get('province')
        location = self.cleaned_data.get('location')

        qs = Location.objects.filter(province=province, location__iexact=location)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            self.add_error('location', f'La localidad "{location}", ya se encuentra asociada a la provincia "{province}"')

        return cleaned_data