from django.urls import path

from core.sh.views.dependency.views import DependencyListView, DependencyCreateView, DependencyDeleteView, DependencyUpdateView, ajax_dependency_search_edifice, ajax_dependency_search_location

app_name = 'sh'

urlpatterns = [

  path('dependency/list/', DependencyListView.as_view(), name='dependency_list'),
  path('dependency/add/', DependencyCreateView.as_view(), name='dependency_add'),
  path('dependency/edit/<int:pk>/', DependencyUpdateView.as_view(), name='dependency_edit'),
  path('dependency/delete/<int:pk>/', DependencyDeleteView.as_view(), name='dependency_delete'),
# Ajax Route
  path('ajax/search_dependency_location/', ajax_dependency_search_location, name='ajax_search_dependency_location'),
  path('ajax/search_dependency_edifice/', ajax_dependency_search_edifice, name='ajax_search_dependency_edifice')

]