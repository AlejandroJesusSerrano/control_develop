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

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Tipo de Insumo agregado correctamente',
        }
        return JsonResponse(data)
      else:
        return super().form_invalid(form)
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
    context['page_title'] = 'Tipos de Insumos'
    context['title'] = 'Agregar un Tipo de Insumo'
    context['btn_add_id'] = 'sup_type_add'
    context['entity'] = 'Tipos de Insumos'
    context['list_url'] = reverse_lazy('sh:suply_type_list')
    context['form_id'] = 'suplyTypeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    context['saved'] = kwargs.get('saved', None)
    return context

class SuplyTypeUpadateView(UpdateView):
  model = Suply_Type
  form_class = SuplyTypeForm
  template_name = 'suply_type/create.html'
  success_url = reverse_lazy('sh:suply_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Tipo de Insumo actualizado exitosamente',
        }
        return JsonResponse(data)
      else:
        return super().form_invalid(form)
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
    context['page_title'] = 'Tipos de Insumos'
    context['title'] = 'Editar Tipo de Insumo'
    context['btn_add_id'] = 'sup_type_add'
    context['entity'] = 'Tipos de Insumos'
    context['list_url'] = reverse_lazy('sh:suply_type_list')
    context['form_id'] = 'suplyTypeForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'
    context['saved'] = kwargs.get('saved', None)
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