from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import BaseModelForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import DependencyForm
from core.sh.models import Dependency


class DependencyListView(ListView):
  model = Dependency
  template_name = 'dependency/list.html'

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
        for i in Dependency.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dependencia'
    context['title'] = 'Listado de Dependencias'
    context['btn_add_id'] = 'dependency_add'
    context['create_url'] = reverse_lazy('sh:dependency_add')
    context['list_url'] = reverse_lazy('sh:dependency_list')
    context['entity'] = 'Dependencias'
    context['nav_icon'] = 'fa-solid fa-gavel'
    context['table_id'] = 'dependency_table'
    return context

class DependencyCreateView(CreateView):
  model: Dependency
  form_class = DependencyForm
  template_name = 'dependency/create.html'
  success_url = reverse_lazy('sh:dependency_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      form.save()
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success':True})
      else:
        return redirect(self.success_url)
    except IntegrityError:
      form.add_error('dependency', 'Ya existe una dependencia con este nombre.')
      return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({
        "error": "Formulario no válido",
        "form_errors": errors
      }, status=400)
    else:
      context = self.get_context_data(form=form)
      context['saved'] = False
      return self.render_to_response(context)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dependencias'
    context['title'] = 'Agregar una Dependencia'
    context['btn_add_id'] = 'dependency_add'
    context['entity'] = 'Dependencias'
    context['list_url'] = reverse_lazy('sh:dependency_list')
    context['form_id'] = 'dependencyForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    context['saved'] = kwargs.get('saved', None)
    return context

class DependencyUpadateView(UpdateView):
  model = Dependency
  form_class = DependencyForm
  template_name = 'dependency/create.html'
  success_url = reverse_lazy('sh:dependency_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      form.save()
    except IntegrityError:
      form.add_error('dependency', 'Esta dependencia ya existe.')
      return self.form_invalid(form)

    if self.request.headers.get('x-requested-with') == 'XMLHttpRedirect':
      return JsonResponse({'success':True})
    else:
      return redirect(self.success_url)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRedirect':
      errors = form.errors.get_json_data()
      return JsonResponse({
        "error": "Formulario no válido",
        "form_errors": errors
      }, status=400)
    else:
      context = self.get_context_data(form=form)
      context['saved'] = False
      return self.render_to_response(context)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Dpenedencias'
      context['title'] = 'Editar Dependencia'
      context['btn_add_id'] = 'dependency_add'
      context['entity'] = 'Dependencias'
      context['list_url'] = reverse_lazy('sh:dependency_list')
      context['form_id'] = 'dependencyForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      context['saved'] = kwargs.get('saved', None)
      return context

class DependencyDeleteView(DeleteView):
  model = Dependency
  template_name = 'dependency/delete.html'
  success_url = reverse_lazy('sh:dependency_list')

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
        context['page_title'] = 'Dependencias'
        context['title'] = 'Eliminar una Dependencia'
        context['del_title'] = 'Dependencia: '
        context['list_url'] = reverse_lazy('sh:dependency_list')
        context['form_id'] = 'dependencyForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context