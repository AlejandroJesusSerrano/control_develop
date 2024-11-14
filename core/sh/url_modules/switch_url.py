from django.urls import include, path

from core.sh.views.switch import views as switch_views

app_name = 'sh'

urlpatterns = [

  path('switch/list/', switch_views.SwitchListView.as_view(), name='switch_list'),
  path('switch/add/', switch_views.SwitchCreateView.as_view(), name='switch_add'),
  path('switch/edit/<int:pk>/', switch_views.SwitchUpdateView.as_view(), name='switch_edit'),
  path('switch/delete/<int:pk>/', switch_views.SwitchDeleteView.as_view(), name='switch_delete'),

]