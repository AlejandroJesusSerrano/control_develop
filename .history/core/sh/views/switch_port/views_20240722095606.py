import logging
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import SwitchPortForm
from core.sh.models import Switch_Port

logger = logging.getLogger(__name__)

class Switch_PortListView(ListView):
  model = Switch_Port
  template_name = 'switch_port/list.html'

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
        for i in Switch_Port.objects.all():
          try:
            data.append(i.toJSON())
          except Exception as e:
            logger.error(f'Error serializing Patch_Port with id {i.id}: {e}')
            raise e
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      logger.error(f'Exception in Patch_PortListView POST: {e}')
      return JsonResponse({'error':str(e)}, status = 500)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Puertos de Switchs'
    context['title'] = 'Listado de Puertos de Switchs'
    context['btn_add_id'] = 'switch_port_add'
    context['create_url'] = reverse_lazy('sh:switch_port_add')
    context['list_url'] = reverse_lazy('sh:switch_port_list')
    context['entity'] = 'Puertos de Switchs'
    context['nav_icon'] = 'fa-solid fa-ethernet'
    context['table_id'] = 'switch_port_table'
    return context

class Switch_PortCreateView(CreateView):
  model: Switch_Port
  form_class = SwitchPortForm
  template_name = 'switch_port/create.html'
  success_url = reverse_lazy('sh:switch_port_list')

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
    context['page_title'] = 'Puertos de Switchs'
    context['title'] = 'Agregar un Puerto de Switch'
    context['btn_add_id'] = 'switch_port_add'
    context['entity'] = 'Puertos de Switchs'
    context['list_url'] = reverse_lazy('sh:switch_port_list')
    context['form_id'] = 'switch_portForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class Switch_PortUpadateView(UpdateView):
  model = Switch_Port
  form_class = SwitchPortForm
  template_name = 'switch_port/create.html'
  success_url = reverse_lazy('sh:switch_port_list')

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
      context['page_title'] = 'Puertos de Switchs'
      context['title'] = 'Editar el Nombre de un Puerto de Switch'
      context['btn_add_id'] = 'switch_port_add'
      context['entity'] = 'Puertos de Switchs'
      context['list_url'] = reverse_lazy('sh:switch_port_list')
      context['form_id'] = 'switch_portForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class Switch_PortDeleteView(DeleteView):
  model = Switch_Port
  template_name = 'switch_port/delete.html'
  success_url = reverse_lazy('sh:switch_port_list')

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
        context['page_title'] = 'Puertos de Switchs'
        context['title'] = 'Eliminar un Puerto de Switch'
        context['del_title'] = 'Puerto Switch: '
        context['list_url'] = reverse_lazy('sh:switch_port_list')
        context['form_id'] = 'switch_portForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context