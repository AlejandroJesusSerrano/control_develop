from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import OfficeLocForm
from core.sh.models import Office_Loc


class OfficeLocListView(ListView):
  model = Office_Loc
  template_name = 'office_loc/list.html'

  # @method_decorator(login_required)
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Office.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Oficinas'
    context['title'] = 'Listado de Oficinas'
    context['btn_add_id'] = 'office_add'
    context['create_url'] = reverse_lazy('sh:office_add')
    context['list_url'] = reverse_lazy('sh:office_list')
    context['entity'] = 'Oficinas'
    context['nav_icon'] = 'fa-regular fa-building'
    context['table_id'] = 'office_table'
    return context

class OfficeCreateView(CreateView):
  model: Office
  form_class = OfficeForm
  template_name = 'office/create.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data={}
    try:
      action = request.POST.get('action')
      if action == 'add':
        form = self.get_form()
        data = form.save()
      else:
        data['error'] = 'Acción no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Oficinas'
    context['title'] = 'Agregar una Oficina'
    context['btn_add_id'] = 'office_add'
    context['entity'] = 'Oficinas'
    context['list_url'] = reverse_lazy('sh:office_list')
    context['form_id'] = 'officeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class OfficeUpadateView(UpdateView):
  model = Office
  form_class = OfficeForm
  template_name = 'office/create.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data={}
    try:
      action = request.POST.get('action')
      if action == 'edit':
        form = self.get_form()
        data = form.save()
      else:
        data['error'] = 'Accion no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Oficinas'
      context['title'] = 'Editar Oficina'
      context['btn_add_id'] = 'office_add'
      context['entity'] = 'Oficinas'
      context['list_url'] = reverse_lazy('sh:office_list')
      context['form_id'] = 'officeForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class OfficeDeleteView(DeleteView):
  model = Office
  template_name = 'office/delete.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data={}
    try:
      self.object.delete()
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Oficinas'
        context['title'] = 'Eliminar una Oficina'
        context['del_title'] = 'Oficina: '
        context['list_url'] = reverse_lazy('sh:office_list')
        context['form_id'] = 'officeForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context