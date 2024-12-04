from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Office, Dependency, Edifice, Location, Province
from core.sh.models.office_loc.models import Office_Loc

class OfficeForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    edifice = forms.ModelChoiceField(
        queryset=Edifice.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    dependency = forms.ModelChoiceField(
        queryset=Dependency.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        required=False
    )

    class Meta:
        model = Office
        fields = [
            'province', 'location', 'edifice', 'dependency', 'loc', 'office', 'description'
        ]
        widgets = {
            'loc': Select(attrs={'class': 'form-control', 'data-placeholder': 'Seleccione la locación de la oficina'}),
            'office': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre identificatorio para la Oficina'}),
            'description': Textarea(attrs={'class':'form-control', 'placeholder': 'Ingrese una descripción de la oficina'})
        }
        help_texts = {
            'description': '* Este campo no es obligatorio, pero puede agregar detalles para individualizar la oficina, o agregar algún dato relevante de la misma.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            if self.instance.loc and self.instance.loc.edifice and self.instance.loc.edifice.location and self.instance.dependency and self.instance.dependency.location:
                province = self.instance.loc.edifice.location.province
                self.fields['location'].queryset = Location.objects.filter(province=province).order_by('location')
                self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.loc.edifice.location).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.dependency.location).order_by('dependency')

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['location'].queryset = Location.objects.filter(province_id=province_id).order_by('location')
                self.fields['edifice'].queryset = Edifice.objects.filter(location__province_id=province_id).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location__province_id=province_id).order_by('dependency')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['location'].queryset = self.instance.loc.edifice.location.province.location_set.order_by('location')

        if 'location' in self.data:
            try:
                location_id = int(self.data.get('location'))
                self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id).order_by('edifice')
                self.fields['dependency'].queryset = Dependency.objects.filter(location_id=location_id).order_by('dependency')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['edifice'].queryset = Edifice.objects.filter(location=self.instance.loc.edifice.location).order_by('edifice')
            self.fields['dependency'].queryset = Dependency.objects.filter(location=self.instance.loc.edifice.location).order_by('dependency')

        if 'edifice' in self.data:
            try:
                edifice_id = int(self.data.get('edifice'))
                self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id).order_by('office_location')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=self.instance.loc.edifice).order_by('edifice')

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
