from django import views
from django.urls import path

from core.sh.views.modals.views import dependency_modal_create, edifice_modal_create, location_modal_create, office_loc_modal_create, province_modal_create

urlpatterns = [
    path('province/modal/add/', province_modal_create, name='province_modal_add'),
    path('location/modal/add/', location_modal_create, name='location_modal_add'),
    path('dependency/modal/add/', dependency_modal_create, name='dependency_modal_add'),
    path('office_loc/modal/add/', office_loc_modal_create, name='office_loc_modal_add'),
    path('edifice/modal/add/', edifice_modal_create, name='edifice_modal_add'),
]
