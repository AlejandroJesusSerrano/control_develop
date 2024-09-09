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
from core.sh.models import Dependency, Location


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
    print(request.POST)
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')

        if action == 'search_location':
          province_id = request.POST.get('province_id')
          locations = Location.objects.filter(province_id=province_id)
          data = [{'id': l.id, 'name': l.location} for l in locations]

        else:
          form = DependencyForm(request.POST)

          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Dependencia guardada correctamente"})
            except Exception as e:
              return JsonResponse({"error": f"Error al intentar guardar la dependencia: {str(e)}"}, status=400)

          else:
            errors = form.errors.get_json_data()
            return JsonResponse({"error": "Formulario no válido", "form_errors": errors}, status=400)

        return JsonResponse(data, safe=False)

      except Exception as e:
        return JsonResponse({'error': str(e)}, status=400, safe=False)

    else:
      return super().post(request, *args, **kwargs)

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
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')

        if action == 'search_location':
          province_id = request.POST.get('province_id')
          locations = Location.objects.filter(province_id=province_id)
          data = [{'id':l.id, 'name': l.location} for l in locations]

        else:
          self.object = self.get_object()
          form = self.get_form()
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Dependencia actualizada correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error": f"Error al actualizar la dependencia de oficina: {str(e)}"}, status=400)
          else:
            errors = form.errors.get_json_data()
            return JsonResponse({"error": "Formulario no válido", "form_errors": errors}, status=400)

        return JsonResponse(data, safe=False)

      except Exception as e:
        data = {'error': str(e)}
        return JsonResponse(data, safe=False)
    else:
      return super().post(request, *args, **kwargs)

  def form_invalid(self, form):
    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({
        "error": "Formulario no válido",
        "form_errors": errors
      }, status=400)
    else:
      context = self.get_context_data(form=form)
      context['saved'] = False
      return self.render_to_response(context)


  def handle_search_action(self, action, post_data):

    data = []

    if action == 'search_edifice':
      province_id = post_data.get('province_id')
      if province_id:
        try:
          province_id = int(province_id)
          locations = Location.objects.filter(province_id=province_id)
          data = [{'id':l.id, 'name': l.location} for l in locations]
        except ValueError:
          pass

    return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dependencias'
    context['title'] = 'Editar Dependencia'
    context['btn_add_id'] = 'dependency_add'
    context['entity'] = 'Dependencia'
    context['list_url'] = reverse_lazy('sh:dependency_list')
    context['form_id'] = 'dependencyForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    dependency = self.get_object()

    context['form'].fields['location'].queryset = Location.objects.filter(
    province = dependency.location.province
    )

    context['form'].initial['province'] = dependency.location.province.id if dependency.location.province else None
    context['form'].initial['location'] = dependency.location.id if dependency.location else None

    context['form'].fields['location'].widget.attrs.update({
      'data-preselected': self.object.location.id if self.object.location else ''
    })

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