from django.urls import path

from core.sh.views.dev_model.views import Dev_ModelsCreateView, Dev_ModelsDetailsView, Dev_ModelsListView, Dev_ModelsUpadateView, Dev_ModelsDeleteView

app_name = 'sh'

urlpatterns = [

  path('dev_model/list/', Dev_ModelsListView.as_view(), name='dev_model_list'),
  path('dev_model/add/', Dev_ModelsCreateView.as_view(), name='dev_model_add'),
  path('dev_model/edit/<int:pk>/', Dev_ModelsUpadateView.as_view(), name='dev_model_edit'),
  path('dev_model/delete/<int:pk>/', Dev_ModelsDeleteView.as_view(), name='dev_model_delete'),
  path('dev_model/details/<int:pk>/', Dev_ModelsDetailsView.as_view(), name='dev_model_details'),

]