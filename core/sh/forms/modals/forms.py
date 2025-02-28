from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Province

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

    def clean(self):
        cleaned_data = super().clean()
        number_id = self.cleaned_data.get('number_id')
        province = self.cleaned_data.get('province').upper()

        qs= Province.objects.all()
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

            if qs.filter(number_id__iexact=number_id).exists():
                self.add_error('number_id', "El id de provincia ya se encuentra registrado")

            if qs.filter(province__iexact=province).exists():
                self.add_error('province', "La provincia ya se encuentra registrada")


        return cleaned_data