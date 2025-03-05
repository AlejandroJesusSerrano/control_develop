from django import views
from django.urls import path

from core.sh.views.modals.views import edifice_modal_create, location_modal_create, province_modal_create

urlpatterns = [
    path('province/modal/add/', province_modal_create, name='province_modal_add'),
    path('location/modal/add/', location_modal_create, name='location_modal_add'),
    path('edifice/modal/add/', edifice_modal_create, name='edifice_modal_add'),
]
