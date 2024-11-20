from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.rack.models import Rack

class PatchPortForm(forms.ModelForm):

  rack = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2'}),
    required = True
  )

  class Meta:
    model = Patch_Port
    fields = [
      'rack', 'patch', 'port'
      ]
    widgets = {
      'patch': Select(attrs={'class': 'form-control select2'}),
      'port': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de puerto'})
    }

  def __init__(self, *args, **kwargs):
    super(PatchPortForm, self).__init__(*args, **kwargs)

    self.fields['rack'].queryset = Rack.objects.all()
    self.fields['patch'].queryset = Patchera.objects.all()

    if self.instance.pk:
      self.initial['rack'] = self.instance.patch.rack
      self.initial['patch'] = self.instance.patch

    else:
      selected_rack = self.data.get('rack')

      try:
        selected_rack = int(selected_rack) if selected_rack else None
      except (ValueError, TypeError):
        selected_rack = None

      if selected_rack:
        self.fields['patch'].queryset = Patchera.objects.filter(rack_id = selected_rack)


  def clean(self):
    cleaned_data = super().clean()

    rack = self.cleaned_data.get('rack')
    patch = self.cleaned_data.get('patch')
    port = self.cleaned_data.get('port')


    if Patch_Port.objects.filter(patch=patch, port=port).exists():
      self.add_error('port', f"* El número de puerto '{port}' que quiere ingresar, ya se encuentra registrado en la patchera: '{patch}' del Rack '{rack}'")

    return cleaned_data