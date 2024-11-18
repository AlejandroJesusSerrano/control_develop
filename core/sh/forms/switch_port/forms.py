from django.forms import *
from django import forms
from django.forms import Select, TextInput, Textarea

from core.sh.models import Switch_Port
from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.dev_type.models import Dev_Type
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patchera.models import Patchera
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack

class SwitchPortForm(forms.ModelForm):

  province = forms.ModelChoiceField(
    queryset = Province.objects.all(),
    widget = forms.Select(attrs = {'class': 'form-control select2'}),
    required = False
  )

  location = forms.ModelChoiceField(
    queryset = Location.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  dependency = forms.ModelChoiceField(
    queryset = Dependency.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  edifice = forms.ModelChoiceField(
    queryset = Edifice.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  loc = forms.ModelChoiceField(
    queryset = Office_Loc.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  office = forms.ModelChoiceField(
    queryset = Office.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  brand = forms.ModelChoiceField(
    queryset = Brand.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  dev_type = forms.ModelChoiceField(
    queryset = Dev_Type.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  dev_model = forms.ModelChoiceField(
    queryset = Dev_Model.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  rack = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  patchera = forms.ModelChoiceField(
    queryset = Patchera.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = False
  )

  class Meta:
    model = Switch_Port
    fields =[
      'province', 'location', 'dependency', 'edifice', 'loc', 'office', 'brand', 'dev_type', 'dev_model', 'rack', 'patchera', 'switch', 'port_id', 'patch_port_out', 'patch_port_in', 'switch_in', 'switch_in', 'switch_out', 'obs'
    ]
    widget = {
      'switch': Select(attrs = {'class': 'form-control select2'}),
      'port_id': TextInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el número de puerto'}),
      'patch_port_out': Select(attrs = {'class': 'form-control select2'}),
      'patch_port_in': Select(attrs = {'class': 'form-control selct2'}),
      'switch_in': Select(attrs = {'class': 'form-control select2'}),
      'switch_out': Select(attrs = {'class': 'form-control select2'}),
      'obs': Textarea(attrs = {'class': 'form-control', 'placeholder': 'Ingrese detalles particulares, si los hubiese'
        }
      )
    }

  def __init__(self, *args, **kwargs):
    super (SwitchPortForm, self).__init__(*args, **kwargs)

    self.fields['province'].queryset = Province.objects.all()
    self.fields['location'].queryset = Location.objects.none()
    self.fields['dependency'].queryset = Dependency.objects.none()
    self.fields['edifice'].queryset = Edifice.objects.none()
    self.fields['loc'].queryset = Office_Loc.objects.none()
    self.fields['office'].queryset = Office.objects.none()
    self.fields['brand'].queryset = Brand.objects.none()

  def save(self, commit=True):
    data={}
    form = super()
    try:
      if form.is_valid():
        form.save()
      else:
        data['error'] = form.errors.get_json_data()
    except Exception as e:
      data['error'] = str(e)
    return data

  def clean(self):
    cleaned_data = super().clean()
    return cleaned_data