from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import SuplyForm
from core.sh.models import Suply


class SuplyListView(ListView):
  model = Suply
  template_name = 'suply/list.html'

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
        for i in Suply.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Insumos'
    context['title'] = 'Listado de Insumos'
    context['btn_add_id'] = 'suply_add'
    context['create_url'] = reverse_lazy('sh:suply_add')
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['entity'] = 'Insumos'
    context['nav_icon'] = 'fa fa-boxes-stacked'
    context['table_id'] = 'suply_table'
    return context

class SuplyCreateView(CreateView):
  model: Suply
  form_class = SuplyForm
  template_name = 'suply/create.html'
  success_url = reverse_lazy('sh:suply_list')

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
    context['page_title'] = 'Insumos'
    context['title'] = 'Agregar un Insumo'
    context['btn_add_id'] = 'suply_add'
    context['entity'] = 'Insumos'
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['form_id'] = 'suplyForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class SuplyUpadateView(UpdateView):
  model = Suply
  form_class = SuplyForm
  template_name = 'suply/create.html'
  success_url = reverse_lazy('sh:suply_list')

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
    context['page_title'] = 'Insumos'
    context['title'] = 'Editar Insumo'
    context['btn_add_id'] = 'suply_add'
    context['entity'] = 'Insumos'
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['form_id'] = 'suplyForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'
    return context

class SuplyDeleteView(DeleteView):
  model = Suply
  template_name = 'suply/delete.html'
  success_url = reverse_lazy('sh:suply_list')

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
    context['page_title'] = 'Insumos'
    context['title'] = 'Eliminar un Insumo'
    context['del_title'] = 'Insumo: '
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['form_id'] = 'suplyForm'
    context['bg_color'] = 'bg-danger'
    context['action'] = 'delete'
    return context