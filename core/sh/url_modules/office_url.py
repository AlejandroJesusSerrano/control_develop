from django.urls import path

from core.sh.views.office.views import OfficeCreateView, OfficeListView, OfficeDeleteView, OfficeUpdateView

app_name = 'sh'

urlpatterns = [

  path('office/list/', OfficeListView.as_view(), name='office_list'),
  path('office/add/', OfficeCreateView.as_view(), name='office_add'),
  path('office/edit/<int:pk>/', OfficeUpdateView.as_view(), name='office_edit'),
  path('office/delete/<int:pk>/', OfficeDeleteView.as_view(), name='office_delete'),

]