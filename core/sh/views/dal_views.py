from dal import autocomplete
from django.db.models import Q

from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province


class ProvinceAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    qs = Province.objects.all()
    if self.q:
      qs = qs.filter(province__istartswith=self.q)
    return qs

class LocationAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    qs = Location.objects.all()

    province = self.forwarded.get('province', None)
    if province:
      qs = qs.filter(province_id=province)

    if self.q:
      qs = qs.filter(location__icontains=self.q)
    return qs

class EdificeAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    qs = Edifice.objects.all()

    province = self.forwarded.get('province', None)
    location = self.forwarded.get('location', None)

    if province:
      qs = qs.filter(location__province_id = province)
    if location:
      qs = qs.filter(location_id=location)

    if self.q:
      qs = qs.filter(edifice__icontains=self.q)
    return qs

class DependencyAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    qs = Dependency.objects.all()

    province = self.forwarded.get('province', None)
    location = self.forwarded.get('location', None)

    if province:
      qs = qs.filter(location__province_id = province)
    if location:
      qs = qs.filter(location_id=location)

    if self.q:
      qs = qs.filter(dependency__icontains=self.q)
    return qs

class OfficeLocAutocomplete(autocomplete.Select2QuerySetView):
  def get_queryset(self):
    qs = Office_Loc.objects.all()

    province = self.forwarded.get('province', None)
    location = self.forwarded.get('location', None)
    edifice = self.forwarded.get('edifice', None)

    if province:
      qs = qs.filter(edifice__location__province_id = province)
    if location:
      qs = qs.filter(edifice__location_id = location)
    if edifice:
      qs = qs.filter(edifice_id = edifice)

    if self.q:
      qs = qs.filter(
        Q(floor__icontains = self.q) |
        Q(wing__icontains = self.q)
      )

    return qs.distinct()