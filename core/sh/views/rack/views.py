from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
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

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Provincia agregada correctamente',
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
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Provincia actualizada exitosamente'
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
      return JsonResponse({"error": errors}, status=400)
    else:
      return super().form_invalid(form)

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