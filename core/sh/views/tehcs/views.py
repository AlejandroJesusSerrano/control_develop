from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import TechsForm
from core.sh.models import Techs


class TechsListView(ListView):
  model = Techs
  template_name = 'techs/list.html'

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
        for i in Techs.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Técnicos'
    context['title'] = 'Listado de Técnicos'
    context['btn_add_id'] = 'techs_add'
    context['create_url'] = reverse_lazy('sh:techs_add')
    context['list_url'] = reverse_lazy('sh:techs_list')
    context['entity'] = 'Técnicos'
    context['nav_icon'] = 'fa fa-helmet-safety'
    context['table_id'] = 'techs_table'
    return context

class TechsCreateView(CreateView):
  model: Techs
  form_class = TechsForm
  template_name = 'techs/create.html'
  success_url = reverse_lazy('sh:techs_list')

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
    context['page_title'] = 'Técnicos'
    context['title'] = 'Agregar un Técnico'
    context['btn_add_id'] = 'techs_add'
    context['entity'] = 'Técnicos'
    context['list_url'] = reverse_lazy('sh:techs_list')
    context['form_id'] = 'techsForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class TechsUpadateView(UpdateView):
  model = Techs
  form_class = TechsForm
  template_name = 'techs/create.html'
  success_url = reverse_lazy('sh:techs_list')

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
      context['page_title'] = 'Técnicos'
      context['title'] = 'Editar Técnico'
      context['btn_add_id'] = 'Techs_add'
      context['entity'] = 'Técnicos'
      context['list_url'] = reverse_lazy('sh:techs_list')
      context['form_id'] = 'techsForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class TechsDeleteView(DeleteView):
  model = Techs
  template_name = 'techs/delete.html'
  success_url = reverse_lazy('sh:techs_list')

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
        context['page_title'] = 'Técnicos'
        context['title'] = 'Eliminar un Técnico'
        context['del_title'] = 'Técnico: '
        context['list_url'] = reverse_lazy('sh:techs_list')
        context['form_id'] = 'techsForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context