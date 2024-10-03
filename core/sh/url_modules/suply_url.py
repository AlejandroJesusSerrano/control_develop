from django.urls import include, path

from core.sh.views.suply.views import SuplyCreateView, SuplyDeleteView, SuplyListView, SuplyUpadateView

app_name = 'sh'

urlpatterns = [

  path('suply/list/', SuplyListView.as_view(), name='suply_list'),
  path('suply/add/', SuplyCreateView.as_view(), name='suply_add'),
  path('suply/edit/<int:pk>/', SuplyUpadateView.as_view(), name='suply_edit'),
  path('suply/delete/<int:pk>/', SuplyDeleteView.as_view(), name='suply_delete'),

]