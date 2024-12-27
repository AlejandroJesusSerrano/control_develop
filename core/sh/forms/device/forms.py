from django.forms import *
from django import forms
from django.forms import Select, TextInput

from django.db.models import Q
from core.sh.models import Dependency, Device, Office, Brand, Dev_Type, Employee, Switch_Port, Dev_Model, Wall_Port
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch

class DeviceForm(forms.ModelForm):

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

    edifice_ports = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice_ports'}),
        required=False
    )

    loc_ports = forms.ModelChoiceField(
        queryset=Office_Loc.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc_ports'}),
        required=False
    )

    office_ports = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_office_ports'}),
        required=False
    )

    rack_ports = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack_ports'}),
        required=False
    )

    switch_ports = forms.ModelChoiceField(
        queryset=Switch.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_ports'}),
        required=False
    )

    patchera_ports = forms.ModelChoiceField(
        queryset=Patchera.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_patchera_ports'}),
        required=False
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.exclude(models_brand__dev_type__dev_type='SWITCH').distinct(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_brand'}),
        required=False
    )

    dev_type = forms.ModelChoiceField(
        queryset=Dev_Type.objects.exclude(dev_type='SWITCH'),
        widget=forms.Select(attrs={'class':'form-control select2', 'id': 'id_dev_type'}),
        required=False
    )

    dev_model = forms.ModelChoiceField(
        queryset=Dev_Model.objects.exclude(dev_type__dev_type='SWITCH'),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dev_model'}),
        required=True
    )

    class Meta:
        model = Device
        fields = [
            'province', 'location', 'dependency', 'edifice', 'loc', 'dev_model', 'connection', 'ip', 'net_name', 'dev_status', 'serial_n', 'office', 'edifice_ports', 'loc_ports', 'office_ports', 'rack_ports', 'switch_ports', 'wall_port_in', 'switch_port_in', 'patchera_ports', 'patch_port_in', 'employee'
        ]
        widgets = {
            'connection': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_connection'
            }),
            'ip': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Si tuviera, ingrese la dirección ip del dispositivo',
                'id': 'id_ip_input'
            }),
            'net_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Si tuviera, ingrese el nombre de registro en la red del dispositivo',
                'id': 'id_net_name_input'
            }),
            'dev_status': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_dev_status'
            }),
            'serial_n': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de serie',
                'id': 'id_serial_n_input'
            }),
            'office': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_office'
            }),
            'wall_port_in': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_wall_port_in'
            }),
            'switch_port_in': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_switch_port_in'
            }),
            'patch_port_in': Select(attrs={
                'class': 'form-control select2',
                'id': 'id_patch_port_in'
            }),
            'employee': SelectMultiple(attrs={
                'class': 'form-control select2',
                'id': 'id_employee'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'data' in kwargs:
            location_id = kwargs['data'].get('location')
            if location_id:
                try:
                    location = Location.objects.get(id=location_id)
                    self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=location).order_by('edifice')
                    self.fields['loc_ports'].queryset = Office_Loc.objects.filter(edifice__location=location).order_by('office_location')
                    self.fields['office_ports'].queryset = Office.objects.filter(loc__edifice__location=location).order_by('office')
                    self.fields['rack_ports'].queryset = Rack.objects.filter(office__loc__edifice__location=location).order_by('rack')
                    self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office__loc__edifice__location=location).order_by('wall_port')
                    self.fields['switch_ports'].queryset = Switch.objects.filter(office__loc__edifice__location=location).order_by('model')
                    self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__rack__office__loc__edifice__location=location).order_by('port_id')
                    self.fields['patchera_ports'].queryset = Patchera.objects.filter(rack__office__loc__edifice__location=location).order_by('patchera')
                    self.fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera__rack__office__loc__edifice__location=location).order_by('port')

                except Location.DoesNotExist:

                    self.fields['edifice_ports'].queryset = Edifice.objects.all()
                    self.fields['loc_ports'].queryset = Office_Loc.objects.all()
                    self.fields['office_ports'].queryset = Office.objects.all()
                    self.fields['rack_ports'].queryset = Rack.objects.all()
                    self.fields['wall_port_in'].queryset = Wall_Port.objects.all()
                    self.fields['switch_ports'].queryset = Switch.objects.all()
                    self.fields['switch_port_in'].queryset = Switch_Port.objects.all()
                    self.fields['patchera_ports'].queryset = Patchera.objects.all()
                    self.fields['patch_port_in'].queryset = Patch_Port.objects.all()
            else:
                self.fields['edifice_ports'].queryset = Edifice.objects.all()

        if 'instance' in kwargs and kwargs['instance']:
            instance=kwargs['instance']
            if instance.office and instance.office.loc and instance.office.loc.edifice and instance.office.loc.edifice.location and instance.office.loc.edifice.location.province and instance.office.dependency:
                self.fields['province'].queryset = Province.objects.all()
                self.fields['province'].initial = instance.office.loc.edifice.location.province.id

                self.fields['location'].queryset = Location.objects.filter(province=instance.office.loc.edifice.location.province)
                self.fields['location'].initial = instance.office.loc.edifice.location.id

                self.fields['edifice'].queryset = Edifice.objects.filter(location=instance.office.loc.edifice.location)
                self.fields['edifice'].initial = instance.office.loc.edifice.id



                self.fields['edifice_ports'].queryset = Edifice.objects.filter(location=instance.office.loc.edifice.location)
                self.fields['edifice_ports'].initial = instance.office.loc.edifice.id



                self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location=instance.office.loc.edifice.location)
                self.fields['dependency'].initial = instance.office.dependency.id

                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=instance.office.loc.edifice)
                self.fields['loc'].initial = instance.office.loc.id

                self.fields['office'].queryset = Office.objects.filter(loc=instance.office.loc)
                self.fields['office'].initial = instance.office.id

                self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office=instance.office)
                self.fields['wall_port_in'].initial = instance.wall_port_in

                self.fields['employee'].queryset = Employee.objects.filter(office=instance.office)
                self.fields['employee'].initial = [e.id for e in instance.employee.all()]

                self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__office=instance.office)
                self.fields['switch_port_in'].initial = instance.switch_port_in


        self.fields['office'].required = True

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data












#---------------------------------------------------CODIGO ANTERIOR---------------------------------------------------
# from django.forms import *
# from django import forms
# from django.forms import Select, TextInput

# from django.db.models import Q
# from core.sh.models import Dependency, Device, Office, Brand, Dev_Type, Employee, Switch_Port, Dev_Model, Wall_Port
# from core.sh.models.edifice.models import Edifice
# from core.sh.models.location.models import Location
# from core.sh.models.office_loc.models import Office_Loc
# from core.sh.models.patch_port.models import Patch_Port
# from core.sh.models.province.models import Province
# from core.sh.models.rack.models import Rack
# from core.sh.models.switch.models import Switch

# class DeviceForm(forms.ModelForm):

#   province = forms.ModelChoiceField(
#     queryset=Province.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_province'}),
#     required=False
#   )

#   location = forms.ModelChoiceField(
#     queryset=Location.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_location'}),
#     required=False
#   )

#   dependency = forms.ModelChoiceField(
#     queryset=Dependency.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
#     required=False
#   )

#   edifice = forms.ModelChoiceField(
#     queryset=Edifice.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
#     required=False
#   )

#   loc = forms.ModelChoiceField(
#     queryset=Office_Loc.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc'}),
#     required=False
#   )

#   edifice_ports = forms.ModelChoiceField(
#     queryset=Edifice.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice_ports'}),
#     required=False
#   )

#   loc_ports = forms.ModelChoiceField(
#     queryset=Office_Loc.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_loc_ports'}),
#     required=False
#   )

#   office_ports = forms.ModelChoiceField(
#     queryset=Office.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_office_ports'}),
#     required=False
#   )

#   rack_ports = forms.ModelChoiceField(
#     queryset=Rack.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack_ports'}),
#     required=False
#   )

#   switch_ports = forms.ModelChoiceField(
#     queryset=Switch.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_switch_ports'}),
#     required=False
#   )

#   brand = forms.ModelChoiceField(
#     queryset=Brand.objects.exclude(models_brand__dev_type__dev_type='SWITCH').distinct(),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_brand'}),
#     required=False
#   )

#   dev_type = forms.ModelChoiceField(
#     queryset=Dev_Type.objects.exclude(dev_type='SWITCH'),
#     widget=forms.Select(attrs={'class':'form-control select2', 'id': 'id_dev_type'}),
#     required=False
#   )

#   dev_model = forms.ModelChoiceField(
#     queryset=Dev_Model.objects.exclude(dev_type__dev_type='SWITCH'),
#     widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dev_model'}),
#     required=True
#   )

#   class Meta:
#     model = Device
#     fields = [
#       'province', 'location', 'dependency', 'edifice', 'loc', 'dev_model', 'connection', 'ip', 'net_name', 'dev_status', 'serial_n', 'office', 'edifice_ports', 'loc_ports', 'office_ports', 'rack_ports', 'switch_ports', 'wall_port_in', 'switch_port_in', 'patch_port_in', 'employee'
#     ]
#     widgets = {
#       'connection': Select(attrs={
#         'class': 'form-control select2',
#         'id': 'id_connection'
#       }),
#       'ip': TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Si tuviera, ingrese la dirección ip del dispositivo',
#         'id': 'id_ip_input'
#       }),
#       'net_name': TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Si tuviera, ingrese el nombre de registro en la red del dispositivo',
#         'id': 'id_net_name_input'
#       }),
#       'dev_status': Select(attrs={
#         'class': 'form-control select2',
#         'id': 'id_dev_status'
#       }),
#       'serial_n': TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Ingrese el número de serie',
#         'id': 'id_serial_n_input'
#       }),
#       'office': Select(attrs={
#         'class': 'form-control select2',
#         'id': 'id_office'
#       }),
#       'wall_port_in': Select(attrs={
#         'class': 'form-control select2',
#         'id': 'id_wall_port_in'
#       }),
#       'switch_port_in': Select(attrs={
#         'class': 'form-control select2',
#         'id': 'id_switch_port_in'
#       }),
#       'patch_port_in': Select(attrs={
#         'class': 'form-control select2',
#         'id': 'id_patch_port_in'
#       }),
#       'employee': SelectMultiple(attrs={
#         'class': 'form-control select2',
#         'id': 'id_employee'}),
#     }

#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)

#     if 'province' in self.data:
#       try:
#         province_id = int(self.data.get('province'))
#         self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
#       except (ValueError, TypeError):
#         self.fields['location'].queryset = Location.objects.none()

#     if 'location' in self.data:
#       try:
#         location_id = int(self.data.get('location'))
#         self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
#       except (ValueError, TypeError):
#         self.fields['edifice'].queryset = Edifice.objects.none()

#     dev_type_queryset = Dev_Type.objects.exclude(dev_type='SWITCH')
#     brand_queryset = Brand.objects.exclude(models_brand__dev_type__dev_type='SWITCH').distinct()
#     dev_model_queryset = Dev_Model.objects.exclude(dev_type__dev_type='SWITCH')


#     selected_dev_type = self.data.get('dev_type') or self.initial.get('dev_type')
#     selected_brand = self.data.get('brand') or self.initial.get('brand')

#     if selected_dev_type:
#       dev_type_queryset = dev_type_queryset.filter(pk=selected_dev_type)
#       brand_queryset = brand_queryset.filter(models_brand__dev_type_id=selected_dev_type)
#       dev_model_queryset = dev_model_queryset.filter(dev_type_id=selected_dev_type)

#     if selected_brand:
#         dev_model_queryset = dev_model_queryset.filter(brand_id=selected_brand)

#     self.fields['dev_type'].queryset = dev_type_queryset
#     self.fields['brand'].queryset = brand_queryset
#     self.fields['dev_model'].queryset = dev_model_queryset

#     used_switch_ports = set()

#     device_switch_port_in = Switch_Port.objects.filter(device_switch_port_in__isnull=False).values_list('id', flat=True)
#     used_switch_ports.update(device_switch_port_in)

#     switch_switch_port_in = Switch_Port.objects.filter(switch_switch_port_in__isnull=False).values_list('id', flat=True)
#     used_switch_ports.update(switch_switch_port_in)

#     wall_switch_port_in = Switch_Port.objects.filter(wall_switch_port_in__isnull=False).values_list('id', flat=True)
#     used_switch_ports.update(wall_switch_port_in)

#     patch_port_switch_port_in = Switch_Port.objects.filter(patch_port_switch_port_in__isnull=False).values_list('id', flat=True)
#     used_switch_ports.update(patch_port_switch_port_in)

#     used_switch_ports = Switch_Port.objects.filter(
#       device_switch_port_in__isnull=False
#       ).values_list('id', flat=True)

#     if self.instance.pk and self.instance.switch_port_in:
#       used_switch_ports = list(used_switch_ports)
#       if self.instance.switch_port_in.id in used_switch_ports:
#         used_switch_ports.remove(self.instance.switch_port_in.id)

#     self.fields['switch_port_in'].queryset = Switch_Port.objects.exclude(id__in=used_switch_ports)

#     used_wall_ports = set()

#     device_wall_port_in = Wall_Port.objects.filter(device_wall_port_in__isnull=False).values_list('id', flat=True)
#     used_wall_ports.update(device_wall_port_in)

#     switch_wall_port_in = Wall_Port.objects.filter(switch_port_in__isnull=False).values_list('id', flat=True)
#     used_wall_ports.update(switch_wall_port_in)

#     patch_wall_port_in = Wall_Port.objects.filter(patch_port_in__isnull=False).values_list('id', flat=True)
#     used_wall_ports.update(patch_wall_port_in)

#     if self.instance.pk and self.instance.wall_port_in:
#         current_port_id = self.instance.wall_port_in.id
#         self.fields['wall_port_in'].queryset = Wall_Port.objects.exclude(id__in=used_wall_ports) | Wall_Port.objects.filter(id=current_port_id)
#     else:
#         self.fields['wall_port_in'].queryset = Wall_Port.objects.exclude(id__in=used_wall_ports)

#     used_patch_ports = set()

#     device_patch_port_in = Patch_Port.objects.filter(device_patch_port_in__isnull=False).values_list('id', flat=True)
#     used_patch_ports.update(device_patch_port_in)

#     switch_patch_port_in = Patch_Port.objects.filter(switch_patch_port_in__isnull=False).values_list('id', flat=True)
#     used_patch_ports.update(switch_patch_port_in)

#     wall_patch_port_in = Patch_Port.objects.filter(wall_patch_port_in__isnull=False).values_list('id', flat=True)
#     used_patch_ports.update(wall_patch_port_in)

#     if self.instance.pk and self.instance.patch_port_in:
#       used_patch_ports = list(used_patch_ports)
#       if self.instance.patch_port_in.id in used_patch_ports:
#         used_patch_ports.remove(self.instance.patch_port_in.id)

#     self.fields['patch_port_in'].queryset = Patch_Port.objects.exclude(id__in=used_patch_ports)

#     if 'province' in self.data:
#       try:
#         province_id = int(self.data.get('province'))

#         self.fields['location'].queryset = Location.objects.filter(
#           province_id=province_id
#         ).order_by('location')

#         self.fields['edifice'].queryset = Edifice.objects.filter(
#           location__province_id=province_id
#         ).order_by('edifice')

#         self.fields['edifice_ports'].queryset = Edifice.objects.filter(
#           location__province_id=province_id
#         ).order_by('edifice')

#         self.fields['dependency'].queryset = Dependency.objects.filter(
#           location__province_id=province_id
#         ).order_by('dependency')

#         self.fields['loc'].queryset = Office_Loc.objects.filter(
#           edifice__location__province_id=province_id
#         ).order_by('office_location')

#         self.fields['loc_ports'].queryset = Office_Loc.objects.filter(
#           edifice__location__province_id=province_id
#         ).order_by('office_location')

#         self.fields['office'].queryset = Office.objects.filter(
#           loc__edifice__location__province_id=province_id,
#           dependency__location__province_id=province_id
#         ).order_by('office')

#         self.fields['office_ports'].queryset = Office.objects.filter(
#           loc__edifice__location__province_id=province_id
#         ).order_by('office')

#         self.fields['rack_ports'].queryset = Rack.objects.filter(
#           office__loc__edifice__location__province_id=province_id
#         ).order_by('rack')

#         self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
#           office__loc__edifice__location__province_id=province_id
#         ).order_by('wall_port')

#         self.fields['switch_ports'].queryset = Switch.objects.filter(
#           office__loc__edifice__location__province_id=province_id
#         ).order_by('model')

#         self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
#           switch__rack__office__loc__edifice__location__province_id=province_id
#         ).order_by('port_id')
#       except (ValueError, TypeError):
#         pass

#     if 'location' in self.data:
#       try:
#         location_id = int(self.data.get('location'))

#         self.fields['edifice'].queryset = Edifice.objects.filter(
#           location_id=location_id
#         ).order_by('edifice')

#         self.fields['loc'].queryset = Office_Loc.objects.filter(
#           edifice__location_id=location_id
#         ).order_by('office_location')

#         self.fields['edifice_ports'].queryset = Edifice.objects.filter(
#           location_id=location_id
#         ).order_by('edifice')

#         self.fields['loc_ports'].queryset = Office_Loc.objects.filter(
#           edifice__location_id=location_id
#         ).order_by('office_location')

#         self.fields['dependency'].queryset = Dependency.objects.filter(
#           location_id=location_id
#         ).order_by('dependency')

#         self.fields['office'].queryset = Office.objects.filter(
#           loc__edifice__location_id=location_id,
#           dependency__location_id=location_id
#         ).order_by('office')

#         self.fields['office_ports'].queryset = Office.objects.filter(
#           loc__edifice__location_id=location_id
#         ).order_by('office')

#         self.fields['rack_ports'].queryset = Rack.objects.filter(
#           office__loc__edifice__location_id=location_id
#         ).order_by('rack')

#         self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
#           office__loc__edifice__location_id=location_id
#         ).order_by('wall_port')

#         self.fields['switch_ports'].queryset = Switch.objects.filter(
#           office__loc__edifice__location_id=location_id
#         ).order_by('model')

#         self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
#           switch__rack__office__loc__edifice__location_id=location_id
#         ).order_by('port_id')

#       except (ValueError, TypeError):
#         pass

#     if 'dependency' in self.data:
#       try:
#         dependency_id = int(self.data.get('dependency'))

#         self.fields['office'].queryset = Office.objects.filter(
#           dependency_id=dependency_id
#         ).order_by('office')

#         self.fields['rack'].queryset = Rack.objects.filter(
#           office__dependency_id=dependency_id
#         ).order_by('rack')

#       except (ValueError, TypeError):
#         pass

#     if 'edifice' in self.data:
#       try:

#         edifice_id = int(self.data.get('edifice'))

#         self.fields['loc'].queryset = Office_Loc.objects.filter(
#           edifice_id=edifice_id
#         ).order_by('office_location')

#         self.fields['office'].queryset = Office.objects.filter(
#           loc__edifice_id=edifice_id
#         ).order_by('office')

#       except (ValueError, TypeError):
#         pass

#     if 'loc' in self.data:
#       try:

#         loc_id = int(self.data.get('loc'))

#         self.fields['office'].queryset = Office.objects.filter(
#           loc_id=loc_id
#         ).order_by('office')

#       except (ValueError, TypeError):
#         pass

#     if 'edifice_ports' in self.data:
#       try:
#         edifice_ports_id = int(self.data.get('edifice_ports'))
#         self.fields['loc_ports'].queryset = Office_Loc.objects.filter(
#           edifice_id=edifice_ports_id
#         ).order_by('office_location')

#         self.fields['office_ports'].queryset = Office.objects.filter(
#           loc__edifice_id=edifice_ports_id
#         ).order_by('office')

#         self.fields['rack_ports'].queryset = Rack.objects.filter(
#           office__loc__edifice_id=edifice_ports_id
#         ).order_by('rack')

#         self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
#           office__loc__edifice_id=edifice_ports_id
#         ).order_by('wall_ports')

#         self.fields['switch_ports'].queryset = Switch.objects.filter(
#           office__loc__edifice_id=edifice_ports_id
#         ).order_by('model')

#         self.fields['switch_ports_in'].queryset = Switch_Port.objects.filter(
#           switch__rack__office__loc__edifice_id=edifice_ports_id
#         ).order_by('port_id')

#         self.fields['patchera_port'].queryset = Patch_Port.objects.filter(
#           patchera__rack__office__loc__edifice_id=edifice_ports_id
#         ).order_by('port')

#       except (ValueError, TypeError):
#         pass

#     if 'loc_ports' in self.data:
#       try:

#         loc_ports_id = int(self.data.get('loc_ports'))

#         self.fields['office_ports'].queryset = Office.objects.filter(
#           loc_id=loc_ports_id
#         ).order_by('office')

#         self.fields['rack_ports'].queryset = Rack.objects.filter(
#           office__loc_id=loc_ports_id
#         ).order_by('rack')

#         self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
#           office__loc_id=loc_ports_id
#         ).order_by('wall_port')

#         self.fields['switch_ports'].queryset = Switch.objects.filter(
#           office__loc_id=loc_ports_id
#         ).order_by('model')

#         self.fields['switch_ports_in'].queryset = Switch_Port.objects.filter(
#           switch__rack__office__loc_id=loc_ports_id
#         ).order_by('port_id')

#       except (ValueError, TypeError):
#         pass

#     if 'office_ports' in self.data:
#       try:

#         office_ports_id = int(self.data.get('office_ports'))

#         self.fields['rack_ports'].queryset = Rack.objects.filter(
#           office_id=office_ports_id
#         ).order_by('rack')

#         self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(
#           office_id=office_ports_id
#         ).order_by('wall_port')

#         self.fields['switch_ports'].queryset = Switch.objects.filter(
#           office_id=office_ports_id
#         ).order_by('model')

#         self.fields['switch_ports_in'].queryset = Switch_Port.objects.filter(
#           switch__rack__office_id=office_ports_id
#         ).order_by('port_id')

#       except (ValueError, TypeError):
#         pass

#     if 'rack_ports' in self.data:
#       try:

#         rack_ports_id = int(self.data.get('rack_ports'))

#         self.fields['switch_ports'].queryset = Switch.objects.filter(
#           rack_id=rack_ports_id
#         ).order_by('model')

#         self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(
#           switch__rack_id=rack_ports_id
#         ).order_by('port_id')

#       except (ValueError, TypeError):
#         pass

#     if 'switch_ports' in self.data:
#       try:

#         switch_ports_id = int(self.data.get('switch_ports'))

#         self.fields['switch_ports_in'].queryset = Switch_Port.objects.filter(
#           switch_id=switch_ports_id
#         ).order_by('port_id')
#       except (ValueError, TypeError):
#         pass

#     if self.instance.pk:

#       self.initial['province'] = self.instance.office.loc.edifice.location.province_id
#       self.initial['location'] = self.instance.office.loc.edifice.location_id
#       self.initial['dependency'] = self.instance.office.dependency
#       self.initial['edifice'] = self.instance.office.loc.edifice
#       self.initial['loc'] = self.instance.office.loc
#       self.initial['office'] = self.instance.office
#       self.initial['brand'] = self.instance.dev_model.brand
#       self.initial['dev_type'] = self.instance.dev_model.dev_type
#       self.initial['dev_model'] = self.instance.dev_model
#       self.initial['employee'] = [e.id for e in self.instance.employee.all()]

#       self.fields['dev_model'].queryset = Dev_Model.objects.filter(
#         brand = self.instance.dev_model.brand,
#         dev_type = self.instance.dev_model.dev_type
#       )

#       self.fields['wall_port_in'].queryset = Wall_Port.objects.filter(office = self.instance.office)
#       self.fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__office = self.instance.office)

#       self.fields['employee'].queryset = Employee.objects.filter(office=self.instance.office)

#   def clean(self):
#     cleaned_data = super().clean()

#     dev_model = cleaned_data.get('dev_model')
#     ip = cleaned_data.get('ip')
#     net_name = cleaned_data.get('net_name')
#     serial_n = cleaned_data.get('serial_n')

#     if Device.objects.filter(dev_model=dev_model, serial_n=serial_n).exists():
#       self.add_error('serial_n', f'Ya existe el dispositivo {dev_model} con el número de serie: {serial_n}.')
#       self.add_error('dev_model', f'Ya se encuentra asignado el número de serie: {serial_n}, para el dispositivo {dev_model}.')

#     if Device.objects.filter(ip=ip).exists():
#       self.add_error('ip', f'la dirección IP: {ip}. Ya de encutra asignada a otro dispositivo.')

#     if Device.objects.filter(net_name=net_name).exists():
#       self.add_error('net_name', f'El nombre de registro en la red: {net_name}. Ya se encuentra asignado a otro dispositivo.')
#     return cleaned_data