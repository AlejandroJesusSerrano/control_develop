from django.urls import path

from core.sh.views.connection_type.views import Connection_TypeCreateView, Connection_TypeDeleteView, Connection_TypeListView, Connection_TypeUpadateView

app_name = 'sh'

urlpatterns = [

  path('connection_type/list/', Connection_TypeListView.as_view(), name='connection_type_list'),
  path('connection_type/add/', Connection_TypeCreateView.as_view(), name='connection_type_add'),
  path('connection_type/edit/<int:pk>/', Connection_TypeUpadateView.as_view(), name='connection_type_edit'),
  path('connection_type/delete/<int:pk>/', Connection_TypeDeleteView.as_view(), name='connection_type_delete')

]