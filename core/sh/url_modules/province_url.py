from django.urls import include, path

from core.sh.views.province.views import ProvinceDeleteView, ProvinceListView, ProvinceCreateView, ProvinceUpdateView

app_name = 'sh'

urlpatterns = [

  path('prov/list/', ProvinceListView.as_view(), name='province_list'),
  path('prov/add/', ProvinceCreateView.as_view(), name='province_add' ),
  path('prov/edit/<int:pk>/', ProvinceUpdateView.as_view(), name='province_edit' ),
  path('prov/delete/<int:pk>/', ProvinceDeleteView.as_view(), name='province_delete' )

]

