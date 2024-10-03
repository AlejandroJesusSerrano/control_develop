
from django.urls import path

from core.sh.views.employee_status.views import EmployeeStatusListView, EmployeeStatusCreateView, EmnployeeStatusUpdateView, EmployeeStatusDeleteView

app_name = 'sh'

urlpatterns = [

  path('employee_status/list/', EmployeeStatusListView.as_view(), name='employee_status_list'),
  path('employee_status/add/', EmployeeStatusCreateView.as_view(), name='employee_status_add'),
  path('employee_status/edit/<int:pk>/', EmnployeeStatusUpdateView.as_view(), name='employee_status_edit'),
  path('employee_status/delete/<int:pk>/', EmployeeStatusDeleteView.as_view(), name='employee_status_delete')

]