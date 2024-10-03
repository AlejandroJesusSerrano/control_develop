from django.urls import path

from core.sh.views.wall_port.views import WallPortCreateView, WallPortDeleteView, WallPortListView, WallPortUpdateView

app_name = 'sh'

urlpatterns = [

  path('wall_port/list/', WallPortListView.as_view(), name='wall_port_list'),
  path('wall_port/add/', WallPortCreateView.as_view(), name='wall_port_add'),
  path('wall_port/edit/<int:pk>/', WallPortUpdateView.as_view(), name='wall_port_edit'),
  path('wall_port/delete/<int:pk>/', WallPortDeleteView.as_view(), name='wall_port_delete')

]