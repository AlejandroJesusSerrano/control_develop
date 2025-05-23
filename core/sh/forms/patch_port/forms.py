from django.forms import *
from django import forms
from django.forms import Select, TextInput

from core.sh.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.rack.models import Rack

class PatchPortForm(forms.ModelForm):

  rack = forms.ModelChoiceField(
    queryset = Rack.objects.all(),
    widget = forms.Select(attrs={'class': 'form-control select2', 'id': 'id_rack'}),
    required = True
  )

  class Meta:
    model = Patch_Port
    fields = [
      'rack', 'patchera', 'port', 'switch_port_in'
      ]
    widgets = {
      'patchera': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_patchera'
      }),
      'port': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese el número de puerto',
        'id': 'id_patch_port_input'
      }),
      'switch_port_in': Select(attrs={
        'class': 'form-control select2',
        'id': 'id_switch_port_in'
      })
    }

  def __init__(self, *args, **kwargs):
    super(PatchPortForm, self).__init__(*args, **kwargs)

    self.fields['rack'].label_from_instance = lambda obj: (
            f"RACK: {obj.rack} EN OFICINA: {obj.office.office}"
        )

    self.fields['rack'].queryset = Rack.objects.all()
    self.fields['patchera'].queryset = Patchera.objects.all()

    if self.instance.pk:
      self.initial['rack'] = self.instance.patchera.rack
      self.initial['patchera'] = self.instance.patchera

    else:
      selected_rack = self.data.get('rack')

      try:
        selected_rack = int(selected_rack) if selected_rack else None
      except (ValueError, TypeError):
        selected_rack = None

      if selected_rack:
        self.fields['patchera'].queryset = Patchera.objects.filter(rack_id = selected_rack)


  def clean(self):
    cleaned_data = super().clean()

    rack = self.cleaned_data.get('rack')
    patchera = self.cleaned_data.get('patchera')
    port = self.cleaned_data.get('port')

    qs = Patch_Port.objects.all()

    if self.instance.pk:
      qs = qs.exclude(pk=self.instance.pk)


    if qs.filter(patchera=patchera, port=port).exists():
      self.add_error('port', f"* El número de puerto '{port}' que quiere ingresar, ya se encuentra registrado en la patchera: '{patchera}' del Rack '{rack}'")

    return cleaned_data