from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import SwitchForm
from core.sh.models import Switch


class SwitchListView(ListView):
  model = Switch
  template_name = 'switch/list.html'

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
        for i in Switch.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Switchs'
    context['title'] = 'Listado de Switchs'
    context['btn_add_id'] = 'switch_add'
    context['create_url'] = reverse_lazy('sh:switch_add')
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['entity'] = 'Switchs'
    context['nav_icon'] = 'fa fa-copyright'
    context['table_id'] = 'switch_table'
    return context

class SwitchCreateView(CreateView):
  model: Switch
  form_class = SwitchForm
  template_name = 'switch/create.html'
  success_url = reverse_lazy('sh:switch_list')

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
    context['page_title'] = 'Switchs'
    context['title'] = 'Agregar una Switch'
    context['btn_add_id'] = 'switch_add'
    context['entity'] = 'Switchs'
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['form_id'] = 'switchForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class SwitchUpadateView(UpdateView):
  model = Switch
  form_class = SwitchForm
  template_name = 'switch/create.html'
  success_url = reverse_lazy('sh:switch_list')

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
      context['page_title'] = 'Switchs '
      context['title'] = 'Editar un Switch'
      context['btn_add_id'] = 'switch_add'
      context['entity'] = 'Switchs'
      context['list_url'] = reverse_lazy('sh:switch_list')
      context['form_id'] = 'switchForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class SwitchDeleteView(DeleteView):
  model = Switch
  template_name = 'switch/delete.html'
  success_url = reverse_lazy('sh:switch_list')

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
        context['page_title'] = 'Switchs'
        context['title'] = 'Eliminar un Switch'
        context['del_title'] = 'Switch: '
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['form_id'] = 'switchForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context