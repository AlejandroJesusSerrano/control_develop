from django.urls import path

from core.sh.views.move_type.views import Move_Type_ListView, Move_Type_CreateView, Move_Type_UpdateView, Move_Type_DeleteView

app_name = 'sh'

urlpatterns = [

  path('move_type/list/', Move_Type_ListView.as_view(), name='move_type_list'),
  path('move_type/add/', Move_Type_CreateView.as_view(), name='move_type_add'),
  path('move_type/edit/<int:pk>/', Move_Type_UpdateView.as_view(), name='move_type_edit'),
  path('move_type/delete/<int:pk>/', Move_Type_DeleteView.as_view(), name='move_type_delete')

]