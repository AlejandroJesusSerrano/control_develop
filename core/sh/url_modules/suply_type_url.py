from django.urls import include, path

from core.sh.views.suply_type.views import SuplyTypeCreateView, SuplyTypeDeleteView, SuplyTypeListView, SuplyTypeUpadateView

app_name = 'sh'

urlpatterns = [

  path('suply_type/list/', SuplyTypeListView.as_view(), name='suply_type_list'),
  path('suply_type/add/', SuplyTypeCreateView.as_view(), name='suply_type_add'),
  path('suply_type/edit/<int:pk>/', SuplyTypeUpadateView.as_view(), name='suply_type_edit'),
  path('suply_type/delete/<int:pk>/', SuplyTypeDeleteView.as_view(), name='suply_type_delete')

]