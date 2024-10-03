from django.urls import path

from core.sh.views.location.views import LocationListView, LocationCreateView, LocationUpadateView, LocationDeleteView

app_name = 'sh'

urlpatterns = [

  path('location/list/', LocationListView.as_view(), name='location_list'),
  path('location/add/', LocationCreateView.as_view(), name='location_add'),
  path('location/edit/<int:pk>/', LocationUpadateView.as_view(), name='location_edit'),
  path('location/delete/<int:pk>/', LocationDeleteView.as_view(), name='location_delete'),

]