from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import PatcheraForm
from core.sh.models import Patchera


class PatcheraListView(ListView):
  model = Patchera
  template_name = 'patchera/list.html'

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
        for i in Patchera.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Patcheras'
    context['title'] = 'Listado de Patcheras'
    context['btn_add_id'] = 'patchera_add'
    context['create_url'] = reverse_lazy('sh:patchera_add')
    context['list_url'] = reverse_lazy('sh:patchera_list')
    context['entity'] = 'Patcheras'
    context['nav_icon'] = 'fa-solid fa-ethernet'
    context['table_id'] = 'patchera_table'
    return context

class PatcheraCreateView(CreateView):
  model: Patchera
  form_class = PatcheraForm
  template_name = 'patchera/create.html'
  success_url = reverse_lazy('sh:patchera_list')

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
    context['page_title'] = 'Patcheras '
    context['title'] = 'Agregar una Patchera'
    context['btn_add_id'] = 'patchera_add'
    context['entity'] = 'Patcheras'
    context['list_url'] = reverse_lazy('sh:patchera_list')
    context['form_id'] = 'patcheraForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class PatcheraUpadateView(UpdateView):
  model = Patchera
  form_class = PatcheraForm
  template_name = 'patchera/create.html'
  success_url = reverse_lazy('sh:patchera_list')

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
      context['page_title'] = 'Patcheras'
      context['title'] = 'Editar una Patchera'
      context['btn_add_id'] = 'patchera_add'
      context['entity'] = 'Patcheras'
      context['list_url'] = reverse_lazy('sh:patchera_list')
      context['form_id'] = 'patcheraForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class PatcheraDeleteView(DeleteView):
  model = Patchera
  template_name = 'patchera/delete.html'
  success_url = reverse_lazy('sh:patchera_list')

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
        context['page_title'] = 'Patcheras '
        context['title'] = 'Eliminar una Patchera'
        context['del_title'] = 'Patchera: '
        context['list_url'] = reverse_lazy('sh:patchera_list')
        context['form_id'] = 'patcheraForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context