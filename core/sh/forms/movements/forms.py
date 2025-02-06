from django import forms
from django.forms import ModelForm, Select, Textarea, DateInput
from core.sh.models import Movements, Device, Switch, Move_Type, Techs, Suply
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

    class EmployeeModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return f"{obj.employee_last_name}, {obj.employee_name} - CUIL Nro: {obj.cuil} / Usuario: {obj.user_pc}"

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
    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_office'}),
        required=False
    )
    employee = EmployeeModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_employee'}),
        required=False
    )
    dev_type = forms.ModelChoiceField(
        queryset=Dev_Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dev_type'}),
        required=False
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.exclude(models_brand__dev_type__dev_type='SWITCH').distinct(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_brand'}),
        required=False
    )
    connection_type = forms.ModelChoiceField(
        queryset=Dev_Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_connection_type'}),
        required=False
    )
    rack = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack'}),
        required=False
    )

    s_serial_n = Switch.objects.values_list('serial_n', flat=True).distinct()
    s_serial_n_choices = [('', '----------')]+[(serial_n, serial_n) for serial_n in s_serial_n]

    switch_serial_n = forms.ChoiceField(
        choices=s_serial_n_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_serial_n'}),
        required=False
    )

    d_serial_n = Device.objects.values_list('serial_n', flat=True).distinct()
    d_serial_n_choices = [('', '----------')]+[(serial_n, serial_n) for serial_n in d_serial_n]

    device_serial_n = forms.ChoiceField(
        choices=d_serial_n_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_device_serial_n'}),
        required=False
    )

    s_rack_pos = Switch.objects.values_list('switch_rack_pos', flat=True).distinct()
    s_rack_pos_choices = [('', '----------')]+[(pos, pos) for pos in s_rack_pos]

    switch_rack_pos = forms.ChoiceField(
        choices=s_rack_pos_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_rack_pos'}),
        required=False
    )

    ips = Device.objects.values_list('ip', flat=True).distinct()
    ip_choices = [('', '----------')]+[(ip, ip) for ip in ips]

    ip = forms.ChoiceField(
        choices=ip_choices,
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_ip'}),
        required=False
    )

    class Meta:
        model = Movements
        fields = [
            'province', 'location', 'dependency', 'edifice', 'loc', 'office', 'employee', 'dev_type', 'brand', 'device', 'switch', 'move', 'techs', 'date', 'suply', 'detail', 'ip', 'connection_type', 'rack', 'switch_serial_n', 'switch_rack_pos', 'device_serial_n'
            ]
        widgets = {
            'device': Select(attrs={'class': 'form-control select2', 'id': 'id_device'}),
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

        if 'instance' in kwargs and kwargs['instance']:
            instance=kwargs['instance']
            if instance.employee and instance.employee.office and instance.employee.office.loc and instance.employee.office.dependency and instance.employee.office.loc.edifice and instance.employee.office.loc.edifice.location and instance.employee.office.loc.edifice.location.province:
                self.fields['province'].queryset = Province.objects.all()
                self.fields['province'].initial = instance.employee.office.loc.edifice.location.province.id

                self.fields['location'].queryset = Location.objects.filter(province=instance.employee.office.loc.edifice.location.province)
                self.fields['location'].initial = instance.employee.office.loc.edifice.location.id

                self.fields['dependency'].queryset = Dependency.objects.filter(location=instance.employee.office.loc.edifice.location)
                self.fields['dependency'].initial = instance.employee.office.loc.edifice.location.dependency.id

                self.fields['edifice'].queryset = Edifice.objects.filter(location=instance.employee.office.loc.edifice.location)
                self.fields['edifice'].initial = instance.employee.office.loc.edifice.id

                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=instance.employee.office.loc.edifice)
                self.fields['loc'].initial = instance.employee.office.loc.id

                self.fields['office'].queryset = Office.objects.filter(loc=instance.employee.office.loc)
                self.fields['office'].initial = instance.employee.office.id

                self.fields['employee'].queryset = Employee.objects.filter(office=instance.employee.office)
                self.fields['employee'].initial = instance.employee

            self.fields['employee'].required = True