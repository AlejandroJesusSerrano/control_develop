from django.urls import include, path

from core.sh.views.rack.views import RackCreateView, RackDeleteView, RackListView, RackUpadateView

app_name = 'sh'

urlpatterns = [

  path('rack/list/', RackListView.as_view(), name='rack_list'),
  path('rack/add/', RackCreateView.as_view(), name='rack_add'),
  path('rack/edit/<int:pk>/', RackUpadateView.as_view(), name='rack_edit'),
  path('rack/delete/<int:pk>/', RackDeleteView.as_view(), name='rack_delete'),

]