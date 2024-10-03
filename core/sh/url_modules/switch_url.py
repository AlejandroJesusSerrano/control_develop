from django.urls import include, path

from core.sh.views.switch import views as switch_views

app_name = 'sh'

urlpatterns = [

  path('switch/list/', switch_views.SwitchListView.as_view(), name='switch_list'),
  path('switch/add/', switch_views.SwitchCreateView.as_view(), name='switch_add'),
  path('switch/edit/<int:pk>/', switch_views.SwitchUpdateView.as_view(), name='switch_edit'),
  path('switch/delete/<int:pk>/', switch_views.SwitchDeleteView.as_view(), name='switch_delete'),
  # Ajax Switch Routes
  path('ajax/search_switch_brand/', switch_views.ajax_switch_search_brand, name='ajax_search_switch_brand'),
  path('ajax/search_switch_model/', switch_views.ajax_switch_search_model, name='ajax_search_switch_model'),
  path('ajax/search_switch_location/', switch_views.ajax_switch_search_location, name='ajax_search_switch_location'),
  path('ajax/search_switch_edifice/', switch_views.ajax_switch_search_edifice, name='ajax_search_switch_edifice'),
  path('ajax/search_switch_dependency/', switch_views.ajax_switch_search_dependency, name='ajax_search_switch_dependency'),
  path('ajax/search_switch_office/', switch_views.ajax_switch_search_office, name='ajax_search_switch_office')

]