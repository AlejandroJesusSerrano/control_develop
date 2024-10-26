from django.urls import path

from core.sh.views.employee.views import EmployeeListView, EmployeeCreateView, EmployeeUpadateView, EmployeeDeleteView, ajax_employee_load_dependency, ajax_employee_load_edifices, ajax_employee_load_loc, ajax_employee_load_office, ajax_employee_search_location

app_name = 'sh'

urlpatterns = [

  path('employee/list/', EmployeeListView.as_view(), name='employee_list'),
  path('employee/add/', EmployeeCreateView.as_view(), name='employee_add'),
  path('employee/edit/<int:pk>/', EmployeeUpadateView.as_view(), name='employee_edit'),
  path('employee/delete/<int:pk>/', EmployeeDeleteView.as_view(), name='employee_delete'),
  #Ajax Routes
  path('ajax/search_employee_location/', ajax_employee_search_location, name="employee_search_location" ),
  path('ajax/employee_load_dependency/', ajax_employee_load_dependency, name="employee_load_dependency"),
  path('ajax/employee_load_edifices/', ajax_employee_load_edifices, name="employee_load_edifices" ),
  path('ajax/employee_load_loc/', ajax_employee_load_loc, name="employee_load_loc"),
  path('ajax/employee_load_office/', ajax_employee_load_office, name="employee_load_office")

]