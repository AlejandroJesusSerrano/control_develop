# core/sh/forms/movements/forms.py
from django import forms
from django.forms import ModelForm, Select, Textarea, DateInput
from core.sh.models.connection_type.models import Connection_Type
from core.sh.models.movements.models import Movements
from core.sh.models.device.models import Device
from core.sh.models.switch.models import Switch
from core.sh.models.move_type.models import Move_Type
from core.sh.models.tehcs.models import Techs
from core.sh.models.suply.models import Suply
from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_type.models import Dev_Type
from core.sh.models.edifice.models import Edifice
from core.sh.models.employee.models import Employee
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack

class MovementsForm(ModelForm):
    # Campos extras para filtrar (no pertenecen al modelo Movements)
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
        required=False
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_location'}),
        required=False
    )
    dependency = forms.ModelChoiceField(
        queryset=Dependency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
        required=False
    )
    edifice = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
        required=False
    )
    loc = forms.ModelChoiceField(
        queryset=Office_Loc.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
        required=False
    )

    class Meta:
        model = Movements
        fields = [
            'office', 'employee', 'device', 'switch', 'move', 'techs', 'date', 'suply', 'detail', 'province', 'location', 'dependency', 'edifice', 'loc'
        ]

        widgets = {
            'office': Select(attrs={'class': 'form-control select2', 'id': 'id_office'}),
            'employee': Select(attrs={'class': 'form-control select2', 'id': 'id_employee'}),
            'device': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_device',
                'data-preselected': ''
                }),
            'switch': Select(attrs={'class': 'form-control select2', 'id': 'id_switch'}),
            'move': Select(attrs={'class': 'form-control select2', 'id': 'id_move'}),
            'techs': Select(attrs={'class': 'form-control select2', 'id': 'id_techs'}),
            'date': DateInput(attrs={
                'class': 'form-control datepicker',
                'id': 'id_date',
                'autocomplete': 'off',
                'data-provide': 'datepicker',
                'data-date-format': 'dd/mm/yyyy'
            }),
            'suply': Select(attrs={'class': 'form-control select2', 'id': 'id_suply'}),
            'detail': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detalle del movimiento...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
