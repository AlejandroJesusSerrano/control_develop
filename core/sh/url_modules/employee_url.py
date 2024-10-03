from django.urls import path

from core.sh.views.employee.views import EmployeeListView, EmployeeCreateView, EmployeeUpadateView, EmployeeDeleteView

app_name = 'sh'

urlpatterns = [

  path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
  path('employee/add/', EmployeeCreateView.as_view(), name='employee_add'),
  path('employee/edit/<int:pk>/', EmployeeUpadateView.as_view(), name='employee_edit'),
  path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete')

]