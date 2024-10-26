from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms.connection_type.forms import ConnectionTypeForm
from core.sh.models import Connection_Type


class Connection_TypeListView(ListView):
  model = Connection_Type
  template_name = 'connection_type/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Connection_Type.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Tipos de Conexión'
    context['title'] = 'Listado de Tipos de Conexión'
    context['btn_add_id'] = 'connection_type_add'
    context['create_url'] = reverse_lazy('sh:connection_type_add')
    context['list_url'] = reverse_lazy('sh:connection_type_list')
    context['entity'] = 'Tipos de Conexión'
    context['nav_icon'] = 'fa-solid fa-ethernet'
    context['table_id'] = 'connection_type_table'
    return context

class Connection_TypeCreateView(CreateView):
  model: Connection_Type
  form_class = ConnectionTypeForm
  template_name = 'connection_type/create.html'
  success_url = reverse_lazy('sh:connection_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Tipo de Conexión agregada correctamente',
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
      return JsonResponse({'error': errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Tipos de Conexión'
    context['title'] = 'Agregar una Tipo de Conexión'
    context['btn_add_id'] = 'connection_type_add'
    context['entity'] = 'Tipos de Conexión'
    context['list_url'] = reverse_lazy('sh:connection_type_list')
    context['form_id'] = 'connection_typeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class Connection_TypeUpadateView(UpdateView):
  model = Connection_Type
  form_class = ConnectionTypeForm
  template_name = 'connection_type/create.html'
  success_url = reverse_lazy('sh:connection_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
        'success': True, 
        'message': 'Tipo de Conexión actualizada exitosamente'
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
      return JsonResponse({"error":errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Tipos de Conexión'
      context['title'] = 'Editar un Tipo de Conexión'
      context['btn_add_id'] = 'connection_type_add'
      context['entity'] = 'Tipos de Conexión'
      context['list_url'] = reverse_lazy('sh:connection_type_list')
      context['form_id'] = 'connection_typeForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class Connection_TypeDeleteView(DeleteView):
  model = Connection_Type
  template_name = 'connection_type/delete.html'
  success_url = reverse_lazy('sh:connection_type_list')

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
        context['page_title'] = 'Tipos de Conexión'
        context['title'] = 'Eliminar un Tipo de Conexión'
        context['del_title'] = 'Tipo de Conexión: '
        context['list_url'] = reverse_lazy('sh:connection_type_list')
        context['form_id'] = 'connection_typeForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context