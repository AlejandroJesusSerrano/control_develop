from django.forms import *
from django import forms
from django.forms import TextInput

from core.sh.models import Brand

class BrandForm(forms.ModelForm):

  class Meta:
    model = Brand
    fields = '__all__'
    widgets = {
      'brand': TextInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Ingrese una Marca',
          'autofocus': True,
          'id': 'id_brand_input'
        }
      ),
    }

  def clean(self):
    brand = self.cleaned_data.get('brand').upper()

    qs = Brand.objects.all()

    if self.instance:
      qs = qs.exclude(pk=self.instance.pk)

    if qs.filter(brand__iexact=brand).exists():
      self.add_error('brand', f"La marca ya se encuentra registrada")

    cleaned_data = super().clean()
    return cleaned_data 

