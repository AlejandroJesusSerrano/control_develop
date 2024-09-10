from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import RackForm
from core.sh.models import Rack


class RackListView(ListView):
  model = Rack
  template_name = 'rack/list.html'

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
        for i in Rack.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Racks'
    context['title'] = 'Listado de Racks'
    context['btn_add_id'] = 'rack_add'
    context['create_url'] = reverse_lazy('sh:rack_add')
    context['list_url'] = reverse_lazy('sh:rack_list')
    context['entity'] = 'Racks'
    context['nav_icon'] = 'fa-solid fa-server'
    context['table_id'] = 'rack_table'
    return context

class RackCreateView(CreateView):
  model: Rack
  form_class = RackForm
  template_name = 'rack/create.html'
  success_url = reverse_lazy('sh:rack_list')

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
    context['page_title'] = 'Racks '
    context['title'] = 'Agregar una Rack'
    context['btn_add_id'] = 'rack_add'
    context['entity'] = 'Racks'
    context['list_url'] = reverse_lazy('sh:rack_list')
    context['form_id'] = 'rackForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class RackUpadateView(UpdateView):
  model = Rack
  form_class = RackForm
  template_name = 'rack/create.html'
  success_url = reverse_lazy('sh:rack_list')

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
      context['page_title'] = 'Racks '
      context['title'] = 'Editar un Rack'
      context['btn_add_id'] = 'rack_add'
      context['entity'] = 'Racks'
      context['list_url'] = reverse_lazy('sh:rack_list')
      context['form_id'] = 'rackForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class RackDeleteView(DeleteView):
  model = Rack
  template_name = 'rack/delete.html'
  success_url = reverse_lazy('sh:rack_list')

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
        context['page_title'] = 'Racks '
        context['title'] = 'Eliminar un Rack'
        context['del_title'] = 'Rack: '
        context['list_url'] = reverse_lazy('sh:rack_list')
        context['form_id'] = 'rackForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context