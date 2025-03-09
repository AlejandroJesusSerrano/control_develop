from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Suply_Type

class SuplyTypeForm(ModelForm):

    class Meta:
        model = Suply_Type
        fields = '__all__'
        widgets = {
            'suply_type': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el tipo de insumo',
                    'autofocus': True,
                    'id': 'id_suply_type_input'
                }
            )
        }

    def clean(self):
        suply_type = self.cleaned_data.get('suply_type')

        suply_type_upper = suply_type.upper()

        qs = Suply_Type.objects.all()

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.filter(suply_type=suply_type_upper).exists():
            self.add_error('suply_type', f"El Tipo de Insumo '{suply_type}', ya se encuentra registrado. Ingrese uno diferente")

        cleaned_data = super().clean()
        return cleaned_data
