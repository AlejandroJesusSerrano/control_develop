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
      'office': Select(attrs={'class': 'form-control select2'}),
      'dependency': Select(attrs={'class': 'form-control select2'}),
      'edifice': Select(attrs={'class': 'form-control select2'}),
      'province': Select(attrs={'class': 'form-control select2'}),
      'location': Select(attrs={'class': 'form-control select2'})
    }
    help_texts = {
      'ports_q': '* Ingrese solo números',
      'switch_rack_pos': '* Ingrese el número de posición del switch en el rack, en caso de encontrarse en uno'
    }

  def __init__(self, *args, **kwargs):
    super(SwitchForm, self).__init__(*args, **kwargs)

    self.fields['brand'].queryset = Brand.objects.all()
    self.fields['model'].queryset = Dev_Model.objects.all()
    self.fields['province'].queryset = Province.objects.all()
    self.fields['office'].queryset = Office.objects.none()
    self.fields['dependency'].queryset = Dependency.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()
    self.fields['loc'].queryset = Office_Loc.objects.none()
    self.fields['location'].queryset = Location.objects.none()
    self.fields['rack'].queryset = Rack.objects.all()

    if self.instance.pk:

      self.fields['province'].initial = self.instance.office.loc.edifice.location.province
      selected_province = self.instance.office.loc.edifice.location.province

      self.fields['location'].queryset = Location.objects.filter(province=selected_province)
      self.fields['location'].initial = self.instance.office.loc.edifice.location
      selected_location = self.instance.office.loc.edifice.location

      self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location=selected_location)
      self.fields['dependency'].initial = self.instance.office.dependency

      self.fields['edifice'].queryset = Edifice.objects.filter(location=selected_location)
      self.fields['edifice'].initial = self.instance.office.loc.edifice
      selected_edifice = self.instance.office.loc.edifice

      self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=selected_edifice)
      self.fields['loc'].initial = self.instance.loc

      self.fields['office'].queryset = Office.objects.filter(loc__edifice=selected_edifice)
      self.fields['office'].initial = self.instance.office

      dev_type = self.instance.model.dev_type
      self.fields['brand'].queryset = Brand.objects.filter(models_brand__dev_type=dev_type).distinct()
      self.fields['brand'].initial = self.instance.model.brand

      if self.instance.model:
        self.fields['model'].queryset = Dev_Model.objects.filter(
        dev_type = dev_type,
        brand = self.instance.model.brand
      )

      if self.instance.office and self.instance.office.loc and self.instance.office.loc.edifice:
        location = self.instance.office.loc.edifice.location
        self.fields['location'].initial = location

        self.fields['edifice'].queryset = Edifice.objects.filter(location=location)
        self.fields['edifice'].initial = self.instance.office.loc.edifice

        self.fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice_id)
        self.fields['loc'].initial = self.instance.office.loc

        self.fields['office'].queryset = Office.objects.filter(loc=loc_id)


      if self.instance.office:
        location = self.instance.office.loc.edifice.location
        self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location=location)
        self.fields['dependency'].initial = self.instance.office.dependency
        self.fields['office'].queryset = Office.objects.filter(
          loc__edifice = self.instance.office.loc.edifice,
          dependency = self.instance.office.dependency
        )
        self.fields['office'].initial = self.instance.office

    else:
      if 'province' in self.data:
        try:
          province_id = int(self.data.get('province'))
          self.fields['location'].queryset = Location.objects.filter(province_id=province_id)
        except (ValueError, TypeError):
          pass
      else:
        self.fields['location'].queryset = Location.objects.none()


      if 'location' in self.data:
        try:
          location_id = int(self.data.get('location'))
          self.fields['dependency'].queryset = Dependency.objects.filter(edifice__location_id=location_id)
          self.fields['edifice'].queryset = Edifice.objects.filter(location_id=location_id)
        except (ValueError, TypeError):
          pass
      else:
        self.fields['dependency'].queryset = Dependency.objects.none()
        self.fields['edifice'].queryset = Edifice.objects.none()

      if 'edifice'in self.data:
        try:
          edifice_id = int(self.data.get('edifice'))
          self.fields['loc'].queryset = Office_Loc.objects.filter(edifice_id=edifice_id)
        except(ValueError, TypeError):
          pass
      else:
        self.fields['edifice'].queryset = Edifice.objects.none()

      if 'loc' in self.data:
        try:
          loc_id = int(self.data.get('loc'))
          self.fields['office'].queryset = Office.objects.filter(loc_id=loc_id)
        except(ValueError, TypeError):
          pass
      else:
        self.filds['loc'].queryset = Office_Loc.objects.none()

  def clean(self):
    cleaned_data = super().clean()
    model = self.cleaned_data.get('model')
    serial_n = self.cleaned_data.get('serial_n')
    rack = self.cleaned_data.get('rack')
    switch_rack_pos = self.cleaned_data.get('switch_rack_pos')

    if Switch.objects.filter(model=model, serial_n=serial_n).exists():
      self.add_error('model', f"Ya se encuentra cargado este modelo de Switch")
      self.add_error('serial_n', f"El número de serie ya se encuentra registrado y asociado al mismo modelo")

    if rack and switch_rack_pos:
      if Switch.objects.filter(rack=rack, switch_rack_pos=switch_rack_pos).exists():
        self.add_error('rack', f"El switch ya se encuentra en el Rack seleccionado")
        self.add_error('switch_rack_pos', f"La posicion seleccionada en el Rack, ya se encuentra ocupada")
    return cleaned_data