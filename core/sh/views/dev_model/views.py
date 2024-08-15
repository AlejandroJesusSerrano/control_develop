from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import Dev_ModelForm
from core.sh.models import Dev_Model


class Dev_ModelsListView(ListView):
  model = Dev_Model
  template_name = 'dev_model/list.html'

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
        for i in Dev_Model.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Modelos de Dispositivos'
    context['title'] = 'Listado de Modelos'
    context['btn_add_id'] = 'dev_model_add'
    context['create_url'] = reverse_lazy('sh:dev_model_add')
    context['list_url'] = reverse_lazy('sh:dev_model_list')
    context['entity'] = 'Modelos de Dispositivos'
    context['nav_icon'] = 'fa-solid fa-laptop-file'
    context['table_id'] = 'dev_model_table'
    return context

class Dev_ModelsCreateView(CreateView):
  model: Dev_Model
  form_class = Dev_ModelForm
  template_name = 'dev_model/create.html'
  success_url = reverse_lazy('sh:dev_model_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data={}
    try:

      action = request.POST.get('action')
      if action == 'add':
        form = self.get_form()

        if form.is_valid():
          form.save()
          data = form.instance.toJSON()
        else:
          data['error'] = form.errors.as_json()

      else:
        data['error'] = 'Acción no válida'

    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Modelos de Dispositivos'
    context['title'] = 'Agregar un Modelo de Dispositivo'
    context['btn_add_id'] = 'dev_model_add'
    context['entity'] = 'Modelos de Dispositivos'
    context['list_url'] = reverse_lazy('sh:dev_model_list')
    context['form_id'] = 'dev_modelForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class Dev_ModelsUpadateView(UpdateView):
  model = Dev_Model
  form_class = Dev_ModelForm
  template_name = 'dev_model/create.html'
  success_url = reverse_lazy('sh:dev_model_list')

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
      context['page_title'] = 'Modelos de Dispositivos'
      context['title'] = 'Editar un Modelo de Dispositivo'
      context['btn_add_id'] = 'dev_model_add'
      context['entity'] = 'Modelos de Dispositivos'
      context['list_url'] = reverse_lazy('sh:dev_model_list')
      context['form_id'] = 'dev_modelForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class Dev_ModelsDeleteView(DeleteView):
  model = Dev_Model
  template_name = 'dev_model/delete.html'
  success_url = reverse_lazy('sh:dev_model_list')

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
        context['page_title'] = 'Modelos de Dispositivos'
        context['title'] = 'Eliminar un Modelo de Dispositivo'
        context['del_title'] = 'Model de Dispositivo: '
        context['list_url'] = reverse_lazy('sh:dev_model_list')
        context['form_id'] = 'dev_modelForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context