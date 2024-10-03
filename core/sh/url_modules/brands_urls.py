from django.urls import path

from core.sh.views.brands.views import BrandListView, BrandCreateView, BrandUpadateView, BrandDeleteView

app_name = 'sh'

urlpatterns = [

  path('brand/list/', BrandListView.as_view(), name='brand_list'),
  path('brand/add/', BrandCreateView.as_view(), name='brand_add'),
  path('brand/edit/<int:pk>/', BrandUpadateView.as_view(), name='brand_edit'),
  path('brand/delete/<int:pk>/', BrandDeleteView.as_view(), name='brand_delete')

]