from urllib import request
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms import DependencyForm
from core.sh.models import Dependency, Province

class DependencyListView(ListView):
  model = Dependency
  template_name = 'dependency/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST.get('action')
      if action == 'searchdata':
        dependencies = Dependency.objects.all()
        data = [d.toJSON() for d in dependencies]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

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
    context['add_btn_title'] = 'Agregar Dependencia'
    return context

class DependencyCreateView(CreateView):
  model = Dependency
  form_class = DependencyForm
  template_name = 'dependency/create.html'
  success_url = reverse_lazy('sh:dependency_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get_template_names(self):
    if self.request.GET.get('popup') == '1':
      return ['dependency/popup_add.html']
    return ['dependency/create.html']


  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data= {
          'success': True,
          'message': 'Dependencia agregada correctamente',
          'dependency_id': self.object.id,
          'dependency_name': self.object.dependency,
          'dependency_location_id': self.object.location.id,
          'dependency_location_name': self.object.location.location,
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      print("Error al guardar:", str(e))
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status=500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({"error": errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dependencias'
    context['title'] = 'Agregar una Dependencia'
    context['btn_add_id'] = 'dependency_add'
    context['entity'] = 'Dependencias'
    context['list_url'] = reverse_lazy('sh:dependency_list')
    context['form_id'] = 'dependencyForm'
    context['action'] = 'add'
    context['btn_color'] = 'btn-primary'
    context['bg_color'] = 'bg-custom-primary'
    context['filter_btn_color'] = 'btn-primary'
    return context

class DependencyUpdateView(UpdateView):
  model = Dependency
  form_class = DependencyForm
  template_name = 'dependency/create.html'
  success_url = reverse_lazy('sh:dependency_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Dependencia actualizada exitosamente',
          'dependency_id': self.object.id,
          'dependency_name': self.object.dependency,
          'dependency_location_id': self.object.location.id,
          'dependency_location_name': self.object.location.location,
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
    context['page_title'] = 'Dependencias'
    context['title'] = 'Editar Dependencia'
    context['btn_add_id'] = 'dependency_add'
    context['entity'] = 'Dependencia'
    context['list_url'] = reverse_lazy('sh:dependency_list')
    context['form_id'] = 'dependencyForm'
    context['action'] = 'edit'
    context['btn_color'] = 'btn-warning'
    context['filter_btn_color'] = 'bg-custom-warning'
    context['bg_color'] = 'bg-custom-warning'

    dependency = self.get_object()

    if dependency and dependency.location:
      province = dependency.location.province
      context['form'].fields['province'].queryset = Province.objects.all()
      context['form'].initial['province'] = province.id

      location = dependency.location
      location = dependency.location
      context['form'].initial['location'] = location.id

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
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context