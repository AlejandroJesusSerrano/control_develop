from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from core.sh.forms.move_type.forms import MoveTypeForm
from core.sh.models.move_type.models import Move_Type


class Move_Type_ListView(ListView):
  model = Move_Type
  template_name='move_type/list.html'

  @method_decorator(csrf_exempt)
  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
     return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Move_Type.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Tipos de Movimientos'
    context['title'] = 'Listado de Tipos de Movimientos'
    context['btn_add_id'] = 'move_type_add'
    context['create_url'] = reverse_lazy('sh:move_type_add')
    context['list_url'] = reverse_lazy('sh:move_type_list')
    context['entity'] = 'Tipos de Movimientos'
    context['nav_icon'] = 'fa-solid fa-arrows-turn-to-dots'
    context['table_id'] = 'move_type_table'
    return context

class Move_Type_CreateView(CreateView):
  model = Move_Type
  form_class = MoveTypeForm
  template_name = 'move_type/create.html'
  success_url = reverse_lazy('sh:move_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
     return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST.get('action')
      if action == 'add':
        form = self.get_form()
        if form.is_valid():
          instance = form.save
          data = instance.toJSON()
        else:
          data['error'] = form.errors
      else:
        data['error'] = 'Acción no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Tipos de Movimientos'
      context['title'] = 'Agregar una Tipo de Movimiento'
      context['btn_add_id'] = 'move_t_add'
      context['entity'] = 'Tipos de Movimientos'
      context['list_url'] = reverse_lazy('sh:move_type_list')
      context['form_id'] = 'move_tForm'
      context['action'] = 'add'
      context['bg_color'] = 'bg-custom-primary'
      return context

class Move_Type_UpdateView(UpdateView):
  model = Move_Type
  form_class = MoveTypeForm
  template_name = 'move_type/create.html'
  success_url = reverse_lazy('sh:move_type_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST.get('action')
      if action == 'add':
        form = self.get_form()
        if form.is_valid():
          instance = form.save
          data = instance.toJSON()
        else:
          data['error'] = form.errors
      else:
        data['error'] = 'Acción no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Tipos de Movimientos'
      context['title'] = 'Editar Datos de una Tipo de Movimiento'
      context['btn_add_id'] = 'move_t_add'
      context['entity'] = 'Tipos de Movimientos'
      context['list_url'] = reverse_lazy('sh:move_type_list')
      context['form_id'] = 'move_tForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-custom-warning'
      return context

class Move_Type_DeleteView(DeleteView):
    model = Move_Type
    template_name = 'move_type/delete.html'
    success_url = reverse_lazy('sh:move_type_list')

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
        context['page_title'] = 'Tipos de Movimientos'
        context['title'] = 'Eliminar una Tipo de Movimiento'
        context['del_title'] = 'Tipo de Movimiento: '
        context['list_url'] = reverse_lazy('sh:move_type_list')
        context['form_id'] = 'move_tForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context
