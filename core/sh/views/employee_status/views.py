from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import EmployeeStatusForm
from core.sh.models import Employee_Status


class EmployeeStatusListView(ListView):
  model = Employee_Status
  template_name = 'employee_status/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Employee_Status.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Estado de los Empleados'
    context['title'] = 'Listado de Estados'
    context['btn_add_id'] = 'employee_status_add'
    context['create_url'] = reverse_lazy('sh:employee_status_add')
    context['list_url'] = reverse_lazy('sh:employee_list')
    context['entity'] = 'Estado de los Empleados'
    context['nav_icon'] = 'fa fa-user-tie'
    context['table_id'] = 'employee_status_table'
    return context

class EmployeeStatusCreateView(CreateView):
  model = Employee_Status
  form_class = EmployeeStatusForm
  template_name = 'employee_status/create.html'
  success_url = reverse_lazy('sh:employee_status_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data={
          'success': True,
          'message': 'Estado agregado exitosamente',
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status = 500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error': errors}, status = 400)
    else:
      return super().form_invalid(form)

  def post(self, request, *args, **kwargs):
    return super().post(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Estado de los Empleados'
    context['title'] = 'Agregar un Estado'
    context['btn_add_id'] = 'employee_status_add'
    context['entity'] = 'Estado de los Empleados'
    context['list_url'] = reverse_lazy('sh:employee_status_list')
    context['form_id'] = 'employeeStatusForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    context['saved'] = kwargs.get('saved', None)
    return context

class EmnployeeStatusUpdateView(UpdateView):
  model = Employee_Status
  form_class = EmployeeStatusForm
  template_name = 'employee_status/create.html'
  success_url = reverse_lazy('sh:employee_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data={
          'success': True,
          'message': 'Estado agregado exitosamente',
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status = 500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error': errors}, status = 400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Estado de los Empleados'
    context['title'] = 'Editar Estado'
    context['btn_add_id'] = 'employee_status_add'
    context['entity'] = 'Estados de los Empleados'
    context['list_url'] = reverse_lazy('sh:employee_status_list')
    context['form_id'] = 'employeeStatusForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'
    context['saved'] = kwargs.get('saved', None)
    return context

class EmployeeStatusDeleteView(DeleteView):
  model = Employee_Status
  template_name = 'employee_status/delete.html'
  success_url = reverse_lazy('sh:employee_status_list')

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
    context['page_title'] = 'Estados de losEmpleados'
    context['title'] = 'Eliminar una Estado'
    context['del_title'] = 'Estado: '
    context['list_url'] = reverse_lazy('sh:employee_status_list')
    context['form_id'] = 'employeeStatusForm'
    context['bg_color'] = 'bg-danger'
    context['action'] = 'delete'
    return context