from django.urls import path

from core.sh.views.office.views import OfficeCreateView, OfficeListView, OfficeDeleteView, OfficeUpdateView, ajax_load_dependency, ajax_load_edifices, ajax_load_loc, ajax_office_search_location

app_name = 'sh'

urlpatterns = [

  path('office/list/', OfficeListView.as_view(), name='office_list'),
  path('office/add/', OfficeCreateView.as_view(), name='office_add'),
  path('office/edit/<int:pk>/', OfficeUpdateView.as_view(), name='office_edit'),
  path('office/delete/<int:pk>/', OfficeDeleteView.as_view(), name='office_delete'),
  # Ajax Routes
  path('ajax/search_office_location/', ajax_office_search_location, name='ajax_search_office_location'),
  path('ajax/load_dependency/', ajax_load_dependency, name='ajax_load_dependency'),
  path('ajax/load_edifice/', ajax_load_edifices, name='ajax_load_edifice'),
  path('ajax/load_loc/', ajax_load_loc, name='ajax_load_loc')

]