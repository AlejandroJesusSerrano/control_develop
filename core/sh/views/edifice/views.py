from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import EdificeForm
from core.sh.models import Edifice


class EdificeListView(ListView):
  model = Edifice
  template_name = 'edifice/list.html'

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
        for i in Edifice.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Edificios'
    context['title'] = 'Listado de edificios'
    context['btn_add_id'] = 'edifice_add'
    context['create_url'] = reverse_lazy('sh:edifice_add')
    context['list_url'] = reverse_lazy('sh:edifice_list')
    context['entity'] = 'Edificios'
    context['nav_icon'] = 'fa fa-building'
    context['table_id'] = 'edifice_table'
    return context

class EdificeCreateView(CreateView):
  model: Edifice
  form_class = EdificeForm
  template_name = 'edifice/create.html'
  success_url = reverse_lazy('sh:edifice_list')

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
    context['page_title'] = 'Edificios'
    context['title'] = 'Agregar un Edificio'
    context['btn_add_id'] = 'edifice_add'
    context['entity'] = 'Edificios'
    context['list_url'] = reverse_lazy('sh:edifice_list')
    context['form_id'] = 'edificeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class EdificeUpadateView(UpdateView):
  model = Edifice
  form_class = EdificeForm
  template_name = 'edifice/create.html'
  success_url = reverse_lazy('sh:edifice_list')

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
      context['page_title'] = 'Edificios'
      context['title'] = 'Editar Edificio'
      context['btn_add_id'] = 'edifice_add'
      context['entity'] = 'Edificios'
      context['list_url'] = reverse_lazy('sh:edifice_list')
      context['form_id'] = 'edificeForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class EdificeDeleteView(DeleteView):
  model = Edifice
  template_name = 'edifice/delete.html'
  success_url = reverse_lazy('sh:edifice_list')

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
        context['page_title'] = 'Edificios'
        context['title'] = 'Eliminar un Edificio'
        context['del_title'] = 'Edificio: '
        context['list_url'] = reverse_lazy('sh:edifice_list')
        context['form_id'] = 'edificeForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context