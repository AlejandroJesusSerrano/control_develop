from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch

class SwitchForm(forms.ModelForm):
  brand = forms.ModelChoiceField(
    queryset = Brand.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  model = forms.ModelChoiceField(
    queryset = Dev_Model.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  dependency = forms.ModelChoiceField(
    queryset = Dependency.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.none(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  class Meta:
    model = Switch
    fields = [
      'brand', 'model', 'serial_n', 'ports_q', 'rack', 'switch_rack_pos', 'loc', 'office', 'dependency', 'edifice', 'location'
      ]
    widgets = {
      'serial_n': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de serie'}),
      'ports_q': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad de puertos del Switch'}),
      'rack': Select(attrs={'class': 'form-control select2'}),
      'switch_rack_pos': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la posición del Switch en el Rack'}),
      'office': Select(attrs={'class': 'form-control select2'})
    }

    help_texts = {
      'ports_q': '* Ingrese solo números',
      'switch_rack_pos': '* Ingrese el número de posición del switch en el rack, en caso de encontrarse en uno'
    }

  def __init__(self, *args, **kwargs):
    super(SwitchForm, self).__init__(*args, **kwargs)

    # Inicializar todos los campos con sus datos completos
    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['model'].queryset = Dev_Model.objects.filter(dev_type__dev_type='SWITCH')
    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.all()
    self.fields['dependency'].queryset = Dependency.objects.all()
    self.fields['edifice'].queryset = Edifice.objects.all()
    self.fields['loc'].queryset = Office_Loc.objects.all()
    self.fields['office'].queryset = Office.objects.all()
    self.fields['rack'].queryset = Rack.objects.all()

    if self.instance.pk:

      if self.instance.office and self.instance.office.loc:
        office = self.instance.office
        loc = office.loc
        edifice = loc.edifice
        location = edifice.location
        province = location.province


        self.fields['province'].initial = province
        self.fields['location'].initial = location
        self.fields['edifice'].initial = edifice
        self.fields['loc'].initial = loc
        self.fields['office'].initial = office

        self.fields['location'].queryset = Location.objects.filter(province=province)
        self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
        self.fields['office'].queryset = Office.objects.filter(loc=loc)

    else:
      if self.data:
        try:
          if 'province' in self.data:
            province_id = int(self.data.get('province'))
            self.fields['location'].queryset = Location.objects.filter(
              province_id=province_id
            )

          if 'location' in self.data:
            location_id = int(self.data.get('location'))
            self.fields['edifice'].queryset = Edifice.objects.filter(
              location_id=location_id
            )
            self.fields['dependency'].queryset = Dependency.objects.filter(
              edifice__location_id=location_id
            )

          if 'edifice' in self.data:
            edifice_id = int(self.data.get('edifice'))
            self.fields['loc'].queryset = Office_Loc.objects.filter(
              edifice_id=edifice_id
            )

          if 'loc' in self.data:
              loc_id = int(self.data.get('loc'))
              self.fields['office'].queryset = Office.objects.select_related(
                'loc', 'dependency'
              ).filter(
                loc_id=loc_id
              )

          if 'dependency' in self.data:
            dependency_id = int(self.data.get('dependency'))
            self.fields['office'].queryset = self.fields['office'].queryset.filter(
              dependency_id=dependency_id
            )

        except (ValueError, TypeError) as e:
          print(f"ERROR en filtrado: {e}")
          pass

  def clean(self):
    cleaned_data = super().clean()
    model = cleaned_data.get('model')
    serial_n = cleaned_data.get('serial_n')
    rack = cleaned_data.get('rack')
    switch_rack_pos = cleaned_data.get('switch_rack_pos')

    if model and serial_n:
      # Excluir el switch actual en caso de edición
      qs = Switch.objects.filter(model=model, serial_n=serial_n)
      if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)

      if qs.exists():
        self.add_error('model', "Ya se encuentra cargado este modelo de Switch")
        self.add_error('serial_n', "El número de serie ya se encuentra registrado y asociado al mismo modelo")

    if rack and switch_rack_pos:
      # Excluir el switch actual en caso de edición
      qs = Switch.objects.filter(rack=rack, switch_rack_pos=switch_rack_pos)
      if self.instance.pk:
        qs = qs.exclude(pk=self.instance.pk)

      if qs.exists():
        self.add_error('rack', "El switch ya se encuentra en el Rack seleccionado")
        self.add_error('switch_rack_pos', "La posición seleccionada en el Rack, ya se encuentra ocupada")

    return cleaned_data
