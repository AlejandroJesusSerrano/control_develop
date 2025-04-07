from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models.switch.models import Switch
from core.sh.models.switch_font.models import SwitchFont

class SwitchFontForm(forms.ModelForm):

    class Meta:
        model = SwitchFont
        fields = [
            'font_name', 'switch', 'font_status', 'send_date', 'reception_date'
        ]
        widgets = {
            'font_name': TextInput(attrs={
                'class': 'form-control',
                'id': 'id_font_name',
                'placeholder': 'Ingrese el nombre de la fuente'
            }),
            'switch': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_switch'
            }),
            'font_status': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_ports_q_input'
            }),
            'send_date': TextInput(attrs={
                'class': 'form-control datepicker',
                'id': 'id_send_date',
                'autocomplete': 'off',
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy',
            }),
            'reception_date': TextInput(attrs={
                'class': 'form-control datepicker',
                'id': 'id_reception_date',
                'autocomplete': 'off',
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy',
            })
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['switch'].queryset = Switch.objects.filter(rack__isnull=False)

        def clean_switch(self):
            switch = self.cleaned_data.get('switch')
            if not switch.rack:
                raise forms.ValidationError('El switch seleccionado no está en un rack.')
            return switch