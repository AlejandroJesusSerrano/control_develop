from django.forms import *
from django import forms
from django.forms import ModelForm, Select, TextInput, FileInput

from core.sh.models import Dev_Model

class Dev_ModelForm(ModelForm):
    class Meta:
        model = Dev_Model

        fields = [
            'dev_type', 'brand', 'dev_model', 'image'
        ]

        widgets = {
            'dev_type': Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'id_dev_type'
                }
            ),
            'brand': Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'id_brand'
                }
            ),
            'dev_model': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el Modelo',
                    'id': 'id_dev_model_input'
                }
            ),
            'image': FileInput(
                attrs={
                    'class': 'form-control-file d-none',
                    'id': 'id_image_selector'
                }
            ),
        }
        help_texts = {
            'image': 'Seleccione archivos de imagen *.jpg, *.bmp, *.png, etc.'
        }

    def clean(self):
        cleaned_data = super().clean()
        dev_type = cleaned_data.get('dev_type')
        brand = cleaned_data.get('brand')
        dev_model = cleaned_data.get('dev_model')

        qs=Dev_Model.objects.all()
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.filter(dev_type=dev_type, brand=brand, dev_model=dev_model):
            self.add_error('dev_type', f"Ya se encuentra registrado un tipo de dispositivo: '{dev_type}', asociado a esta marca y modelo")
            self.add_error('brand', f"Ya se encuentra registrada la marca: '{brand}', para este tipo de dispositivo y modelo")
            self.add_error('dev_model', f"Ya se encuentra registrado el modelo: '{dev_model}', con esta marca y tipo de dispositivo")
        return cleaned_data