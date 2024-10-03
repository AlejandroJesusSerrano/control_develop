from django.urls import path

from core.sh.views.dev_status.views import Dev_StatusCreateView, Dev_StatusDeleteView, Dev_StatusUpadateView, DevStatusListView

app_name = 'sh'

urlpatterns = [

  path('dev_status/list/', DevStatusListView.as_view(), name='dev_status_list'),
  path('dev_status/add/', Dev_StatusCreateView.as_view(), name='dev_status_add'),
  path('dev_status/edit/<int:pk>/', Dev_StatusUpadateView.as_view(), name='dev_status_edit'),
  path('dev_status/delete/<int:pk>/', Dev_StatusDeleteView.as_view(), name='dev_status_delete')

]