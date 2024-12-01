from django.urls import path

from core.sh.views.dal_views import DependencyAutocomplete, EdificeAutocomplete, LocationAutocomplete, OfficeLocAutocomplete, ProvinceAutocomplete

app_name = 'dal'

urlpatterns = [
    path('province-autocomplete/', ProvinceAutocomplete.as_view(), name='province-autocomplete'),
    path('location-autocomplete/', LocationAutocomplete.as_view(), name='location-autocomplete'),
    path('edifice-autocomplete/', EdificeAutocomplete.as_view(), name='edifice-autocomplete'),
    path('dependency-autocomplete/', DependencyAutocomplete.as_view(), name='dependency-autocomplete'),
    path('office-loc-autocomplete/', OfficeLocAutocomplete.as_view(), name='office-loc-autocomplete'),
]
