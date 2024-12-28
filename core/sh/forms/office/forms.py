from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Office, Dependency, Edifice, Location, Province
from core.sh.models.office_loc.models import Office_Loc

class OfficeForm(forms.ModelForm):

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

    edifice = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_edifice'}),
        required=False
    )

    dependency = forms.ModelChoiceField(
        queryset=Dependency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2', 'id': 'id_dependency'}),
        required=True
    )

    class Meta:
        model = Office
        fields = [
            'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'description'
        ]
        widgets = {
            'loc': Select(attrs={
                'class': 'form-control',
                'data-placeholder': 'Seleccione la locación de la oficina',
                'id': 'id_loc'
            }),
            'office': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese un nombre identificatorio para la Oficina',
                'id': 'id_office_input'
            }),
            'description': Textarea(attrs={
                'class':'form-control',
                'placeholder': 'Ingrese una descripción de la oficina',
                'id': 'id_office_description_input'
            })
        }
        help_texts = {
            'description': '* Este campo no es obligatorio, pero puede agregar detalles para individualizar la oficina, o agregar algún dato relevante de la misma.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

                self.fields['dependency'].queryset = Dependency.objects.filter(location=instance.office.loc.edifice.location)
                self.fields['dependency'].initial = instance.office.dependency.id

                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=instance.office.loc.edifice)
                self.fields['loc'].initial = instance.office.loc.id

    def clean(self):
        cleaned_data = super().clean()

        dependency = cleaned_data.get('dependency')
        office = cleaned_data.get('office')

        if office and dependency:
            office = office.strip()
            qs = Office.objects.filter(dependency=dependency, office__iexact=office)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('office', f"Ya existe la oficina en la dependencia seleccionada")

        return cleaned_data
