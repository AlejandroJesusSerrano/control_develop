from django.urls import path

from core.sh.views.dependency.views import DependencyListView, DependencyCreateView, DependencyDeleteView, DependencyUpdateView

app_name = 'sh'

urlpatterns = [

  path('dependency/list/', DependencyListView.as_view(), name='dependency_list'),
  path('dependency/add/', DependencyCreateView.as_view(), name='dependency_add'),
  path('dependency/edit/<int:pk>/', DependencyUpdateView.as_view(), name='dependency_edit'),
  path('dependency/delete/<int:pk>/', DependencyDeleteView.as_view(), name='dependency_delete'),

]