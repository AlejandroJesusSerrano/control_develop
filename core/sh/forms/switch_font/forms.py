from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models.switch.models import Switch
from core.sh.models.switch_font.models import SwitchFont

class SwitchFontForm(forms.ModelForm):

    class Meta:
        model = SwitchFont
        fields = [
            'font_name', 'switch', 'font_status', 'send_date', 'reception_date', 'obs'
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
            'obs': TextInput(attrs={
                'class': 'form-control',
                'id': 'id_obs',
                'placeholder': 'Ingrese una observación'
            })
        }

        send_date = forms.DateField(
            input_formats=['%d/%m/%Y'],
            required=False
        )

        reception_date = forms.DateField(
            input_formats=['%d/%m/%Y'],
            required=False
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        switches = Switch.objects.filter(rack__isnull=False)
        self.fields['switch'].queryset = switches

    def clean_switch(self):
        switch = self.cleaned_data.get('switch')
        font_name = self.cleaned_data.get('font_name')
        qs = SwitchFont.objects.all()
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(switch=switch, font_name=font_name).exists():
            raise forms.ValidationError('Ya se encuentra asociada una fuente con el mismo nombre para este switch.')
        return switch