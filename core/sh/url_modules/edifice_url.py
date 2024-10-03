from django.urls import path

from core.sh.views.edifice.views import EdificeListView, EdificeCreateView, EdificeUpdateView, EdificeDeleteView, ajax_edifice_search_location

app_name = 'sh'

urlpatterns = [

  path('edifice/list/', EdificeListView.as_view(), name='edifice_list'),
  path('edifice/add/', EdificeCreateView.as_view(), name='edifice_add'),
  path('edifice/edit/<int:pk>/', EdificeUpdateView.as_view(), name='edifice_edit'),
  path('edifice/delete/<int:pk>/', EdificeDeleteView.as_view(), name='edifice_delete'),
  # Ajax Route
  path('ajax/search_edifice_location/', ajax_edifice_search_location, name='ajax_search_edifice_location')

]