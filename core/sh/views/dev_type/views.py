from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms import Dev_TypeForm
from core.sh.models import Dev_Type


class Dev_TypeListView(ListView):
  model = Dev_Type
  template_name = 'dev_type/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Dev_Type.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Tipos de Dispositivos'
    context['title'] = 'Listado de Tipos de Dispositivos'
    context['btn_add_id'] = 'dev_type_add'
    context['create_url'] = reverse_lazy('sh:dev_type_add')
    context['list_url'] = reverse_lazy('sh:dev_type_list')
    context['entity'] = 'Tipos de Dispositivos'
    context['nav_icon'] = 'fa fa-microchip'
    context['table_id'] = 'dev_type_table'
    context['add_btn_title'] = 'Agregar Tipo de Dispositivo'
    return context

class Dev_TypeCreateView(CreateView):
  model: Dev_Type
  form_class = Dev_TypeForm
  template_name = 'dev_type/create.html'
  success_url = reverse_lazy('sh:dev_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get_template_names(self):
    if self.request.GET.get('popup') == '1':
      return ['dev_type/popup_add.html']
    return ['dev_type/create.html']

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Tipo de Dispositivo agregado correctamente',
          'dev_type_id': self.object.id,
          'dev_type_name': self.object.dev_type
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
    context['page_title'] = 'Tipos de Dispositivos'
    context['title'] = 'Agregar un Tipo de Dispositivo'
    context['btn_add_id'] = 'dev_type_add'
    context['entity'] = 'Tipos de Dispositivos'
    context['list_url'] = reverse_lazy('sh:dev_type_list')
    context['form_id'] = 'dev_typeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-custom-primary'
    return context

class Dev_TypeUpadateView(UpdateView):
  model = Dev_Type
  form_class = Dev_TypeForm
  template_name = 'dev_type/create.html'
  success_url = reverse_lazy('sh:dev_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'succes': True,
          'message': 'Tipo de Dispositivo actualizado exitosamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error':str(e)}, status=500)
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
      context['page_title'] = 'Tipos de Dispositivos'
      context['title'] = 'Editar Tipo de Dispositivo'
      context['btn_add_id'] = 'dev_type_add'
      context['entity'] = 'Tipos de Dispositivos'
      context['list_url'] = reverse_lazy('sh:dev_type_list')
      context['form_id'] = 'dev_typeForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-custom-warning'
      return context

class Dev_TypeDeleteView(DeleteView):
  model = Dev_Type
  template_name = 'dev_type/delete.html'
  success_url = reverse_lazy('sh:dev_type_list')

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
        context['page_title'] = 'Tipos de Dispositivos'
        context['title'] = 'Eliminar un Tipo de Dispositivo'
        context['del_title'] = 'Tipo de Dispositivo: '
        context['list_url'] = reverse_lazy('sh:dev_type_list')
        context['form_id'] = 'dev_typeForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context