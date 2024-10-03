from django.urls import path

from core.sh.views.dev_type.views import Dev_TypeListView, Dev_TypeCreateView, Dev_TypeUpadateView, Dev_TypeDeleteView

app_name = 'sh'

urlpatterns = [

  path('dev_type/list/', Dev_TypeListView.as_view(), name='dev_type_list'),
  path('dev_type/add/', Dev_TypeCreateView.as_view(), name='dev_type_add'),
  path('dev_type/edit/<int:pk>/', Dev_TypeUpadateView.as_view(), name='dev_type_edit'),
  path('dev_type/delete/<int:pk>/', Dev_TypeDeleteView.as_view(), name='dev_type_delete')

]