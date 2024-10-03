
from django.urls import path

from core.sh.views.office_loc.views import Office_Loc_ListView, Office_Loc_CreateView, Office_Loc_UpdateView, Office_Loc_DeleteView, ajax_office_loc_search_edifice, ajax_office_loc_search_location

app_name = 'sh'

urlpatterns = [

  path('office_loc/list/', Office_Loc_ListView.as_view(), name='office_loc_list'),
  path('office_loc/add/', Office_Loc_CreateView.as_view(), name='office_loc_add'),
  path('office_loc/edit/<int:pk>/', Office_Loc_UpdateView.as_view(), name='office_loc_edit'),
  path('office_loc/delete/<int:pk>/', Office_Loc_DeleteView.as_view(), name='office_loc_delete'),
  # Office_Loc Ajax Routes
  path('ajax/search_office_loc_location/', ajax_office_loc_search_location, name='ajax_search_office_loc_location'),
  path('ajax/search_office_loc_edifice/', ajax_office_loc_search_edifice, name='ajax_office_loc_search_edifice'),

]