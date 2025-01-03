from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms.movements.forms import MovementsForm
from core.sh.models.movements.models import Movements




class MovementsListView(ListView):
  model = Movements
  template_name = 'Movements/list.html'

  # @method_decorator(login_required)
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Movements.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Movimientos'
    context['title'] = 'Listado de Movimientos'
    context['btn_add_id'] = 'Movements_add'
    context['create_url'] = reverse_lazy('sh:movements_add')
    context['list_url'] = reverse_lazy('sh:movements_list')
    context['entity'] = 'Movimientos'
    context['nav_icon'] = 'fa-regular fa-building'
    context['table_id'] = 'Movements_table'
    return context

class MovementsCreateView(CreateView):
  model: Movements
  form_class = MovementsForm
  template_name = 'Movements/create.html'
  success_url = reverse_lazy('sh:movements_list')

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
    context['page_title'] = 'Movimientos'
    context['title'] = 'Agregar una Movimiento'
    context['btn_add_id'] = 'Movements_add'
    context['entity'] = 'Movimientos'
    context['list_url'] = reverse_lazy('sh:movements_list')
    context['form_id'] = 'MovementsForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-custom-primary'
    return context

class MovementsUpdateView(UpdateView):
  model = Movements
  form_class = MovementsForm
  template_name = 'Movements/create.html'
  success_url = reverse_lazy('sh:movements_list')

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
      context['page_title'] = 'Movimientos'
      context['title'] = 'Editar Movimiento'
      context['btn_add_id'] = 'Movements_add'
      context['entity'] = 'Movimientos'
      context['list_url'] = reverse_lazy('sh:movements_list')
      context['form_id'] = 'MovementsForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-custom-warning'
      return context

class MovementsDeleteView(DeleteView):
  model = Movements
  template_name = 'Movements/delete.html'
  success_url = reverse_lazy('sh:movements_list')

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
        context['page_title'] = 'Movimientos'
        context['title'] = 'Eliminar una Movimiento'
        context['del_title'] = 'Movimiento: '
        context['list_url'] = reverse_lazy('sh:movements_list')
        context['form_id'] = 'MovementsForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context