from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms import EmployeeForm
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.employee.models import Employee
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province

class EmployeeListView(ListView):
  model = Employee
  template_name = 'employee/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Employee.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Empleados'
    context['title'] = 'Listado de Empleados'
    context['btn_add_id'] = 'employee_add'
    context['create_url'] = reverse_lazy('sh:employee_add')
    context['list_url'] = reverse_lazy('sh:employee_list')
    context['entity'] = 'Empleados'
    context['nav_icon'] = 'fa fa-user-tie'
    context['table_id'] = 'employee_table'
    return context

class EmployeeCreateView(CreateView):
  model: Employee
  form_class = EmployeeForm
  template_name = 'employee/create.html'
  success_url = reverse_lazy('sh:employee_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Empleado agregado correctamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-reuquested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status=500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error': errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Empleados'
    context['title'] = 'Agregar un Empleado'
    context['btn_add_id'] = 'employee_add'
    context['entity'] = 'Empleados'
    context['list_url'] = reverse_lazy('sh:employee_list')
    context['form_id'] = 'employeeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class EmployeeUpadateView(UpdateView):
  model = Employee
  form_class = EmployeeForm
  template_name = 'employee/create.html'
  success_url = reverse_lazy('sh:employee_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Empleado actualizado correctamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status=500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error':errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Empleados'
    context['title'] = 'Editar Empleado'
    context['btn_add_id'] = 'employee_add'
    context['entity'] = 'Empleados'
    context['list_url'] = reverse_lazy('sh:employee_list')
    context['form_id'] = 'employeeForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    employee = self.get_object()

    if employee.office and employee.office.loc and employee.office.loc.edifice and employee.office.loc.edifice.location and employee.office.loc.edifice.location.province and employee.office.dependency:

      province = employee.office.loc.edifice.location.province
      context['form'].fields['province'].queryset = Province.objects.all()
      context['form'].initial['province'] = province.id

      location = employee.office.loc.edifice.location
      context['form'].fields['location'].queryset = Location.objects.filter(province=province)
      context['form'].initial['location'] = location.id

      edifice = employee.office.loc.edifice
      context['form'].fields['edifice'].queryset = Edifice.objects.filter(location=location)
      context['form'].initial['edifice'] = edifice.id

      dependency = employee.office.dependency
      context['form'].fields['dependency'].queryset = Dependency.objects.filter(edifice__location=location)
      context['form'].initial['dependency'] = dependency.id

      loc = employee.office.loc
      context['form'].fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
      context['form'].initial['loc'] = loc.id

      office = employee.office
      context['form'].fields['office'].queryset = Office.objects.filter(loc=loc)
      context['form'].initial['office'] = office.id

    return context

class EmployeeDeleteView(DeleteView):
  model = Employee
  template_name = 'employee/delete.html'
  success_url = reverse_lazy('sh:employee_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      self.object.delete()
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Empleados'
    context['title'] = 'Eliminar una Empleado'
    context['del_title'] = 'Empleado: '
    context['list_url'] = reverse_lazy('sh:employee_list')
    context['form_id'] = 'employeeForm'
    context['bg_color'] = 'bg-danger'
    context['action'] = 'delete'
    return context