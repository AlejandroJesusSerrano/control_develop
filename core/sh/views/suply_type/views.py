from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import SuplyTypeForm
from core.sh.models import Suply_Type


class SuplyTypeListView(ListView):
  model = Suply_Type
  template_name = 'suply_type/list.html'

  @method_decorator(login_required)
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Suply_Type.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Tipos de Insumos'
    context['title'] = 'Listado de Tipos de Insumos'
    context['btn_add_id'] = 'suply_type_add'
    context['create_url'] = reverse_lazy('sh:suply_type_add')
    context['list_url'] = reverse_lazy('sh:suply_type_list')
    context['entity'] = 'Tipos de Insumos'
    context['nav_icon'] = 'fa fa-user-tie'
    context['table_id'] = 'suply_type_table'
    return context

class SuplyTypeCreateView(CreateView):
  model: Suply_Type
  form_class = SuplyTypeForm
  template_name = 'suply_type/create.html'
  success_url = reverse_lazy('sh:suply_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
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
    context['page_title'] = 'Tipos de Insumos'
    context['title'] = 'Agregar un Tipo de Insumo'
    context['entity'] = 'Tipos de Insumos'
    context['list_url'] = reverse_lazy('sh:suply_type_list')
    context['form_id'] = 'suplyTypeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class SuplyTypeUpadateView(UpdateView):
  model = Suply_Type
  form_class = SuplyTypeForm
  template_name = 'suply_type/create.html'
  success_url = reverse_lazy('sh:suply_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
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
    context['page_title'] = 'Tipos de Insumos'
    context['title'] = 'Editar Tipo de Insumo'
    context['entity'] = 'Tipos de Insumos'
    context['list_url'] = reverse_lazy('sh:suply_type_list')
    context['form_id'] = 'suplyTypeForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'
    return context

class SuplyTypeDeleteView(DeleteView):
  model = Suply_Type
  template_name = 'suply_type/delete.html'
  success_url = reverse_lazy('sh:suply_type_list')

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
    context['page_title'] = 'Tipos de Insumos'
    context['title'] = 'Eliminar un Tipo de Insumo'
    context['del_title'] = 'Tipo de Insumo: '
    context['list_url'] = reverse_lazy('sh:suply_type_list')
    context['form_id'] = 'suplyTypeForm'
    context['bg_color'] = 'bg-danger'
    context['action'] = 'delete'
    return context