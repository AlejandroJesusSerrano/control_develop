from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import PatchPortForm
from core.sh.models import Patch_Port


class Patch_PortListView(ListView):
  model = Patch_Port
  template_name = 'patch_port/list.html'

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
        for i in Patch_Port.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Puertos Patcheras'
    context['title'] = 'Listado de Puertos Patcheras'
    context['btn_add_id'] = 'patch_port_add'
    context['create_url'] = reverse_lazy('sh:patch_port_add')
    context['list_url'] = reverse_lazy('sh:patch_port_list')
    context['entity'] = 'Puertos Patcheras'
    context['nav_icon'] = 'fa fa-copyright'
    context['table_id'] = 'patch_port_table'
    return context

class Patch_PortCreateView(CreateView):
  model: Patch_Port
  form_class = PatchPortForm
  template_name = 'patch_port/create.html'
  success_url = reverse_lazy('sh:patch_port_list')

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
    context['page_title'] = 'Puertos Patcheras'
    context['title'] = 'Agregar un Puerto de Patchera'
    context['btn_add_id'] = 'patch_port_add'
    context['entity'] = 'Puertos Patcheras'
    context['list_url'] = reverse_lazy('sh:patch_port_list')
    context['form_id'] = 'patch_portForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class Patch_PortUpadateView(UpdateView):
  model = Patch_Port
  form_class = PatchPortForm
  template_name = 'patch_port/create.html'
  success_url = reverse_lazy('sh:patch_port_list')

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
      context['page_title'] = 'Puertos Patcheras'
      context['title'] = 'Editar el Puerto de una Patchera'
      context['btn_add_id'] = 'patch_port_add'
      context['entity'] = 'Puertos Patcheras'
      context['list_url'] = reverse_lazy('sh:patch_port_list')
      context['form_id'] = 'patch_portForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class Patch_PortDeleteView(DeleteView):
  model = Patch_Port
  template_name = 'patch_port/delete.html'
  success_url = reverse_lazy('sh:patch_port_list')

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
        context['page_title'] = 'Puertos Patcheras'
        context['title'] = 'Eliminar un Puerto de Patchera'
        context['del_title'] = 'Puerto Patchera: '
        context['list_url'] = reverse_lazy('sh:patch_port_list')
        context['form_id'] = 'patch_portForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context