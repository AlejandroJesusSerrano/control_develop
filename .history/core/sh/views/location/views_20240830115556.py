from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import LocationForm
from core.sh.models import Location


class LocationListView(ListView):
  model = Location
  template_name = 'location/list.html'

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
        for i in Location.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Localidades'
    context['title'] = 'Listado de Localidades'
    context['btn_add_id'] = 'location_add'
    context['create_url'] = reverse_lazy('sh:location_add')
    context['list_url'] = reverse_lazy('sh:location_list')
    context['entity'] = 'Localidades'
    context['nav_icon'] = 'fa-solid fa-earth-americas'
    context['table_id'] = 'location_table'
    return context

class LocationCreateView(CreateView):
  model: Location
  form_class = LocationForm
  template_name = 'location/create.html'
  success_url = reverse_lazy('sh:location_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    form.save()
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      return JsonResponse({'success':True})
    else:
      return redirect(self.success_url)

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
    context['page_title'] = 'Localidades'
    context['title'] = 'Agregar una Localidad'
    context['btn_add_id'] = 'location_add'
    context['entity'] = 'Localidades'
    context['list_url'] = reverse_lazy('sh:location_list')
    context['form_id'] = 'locationForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    context['saved'] = kwargs.get('saved', None)
    return context

class LocationUpadateView(UpdateView):
  model = Location
  form_class = LocationForm
  template_name = 'location/create.html'
  success_url = reverse_lazy('sh:location_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    form.save()
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      return JsonResponse({'success':True})
    else:
      return redirect(self.success_url)

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
      context['page_title'] = 'Localidades'
      context['title'] = 'Editar Localidad'
      context['btn_add_id'] = 'location_add'
      context['entity'] = 'Localidades'
      context['list_url'] = reverse_lazy('sh:location_list')
      context['form_id'] = 'locationForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      context['saved'] = kwargs.get('saved', None)
      return context

class LocationDeleteView(DeleteView):
  model = Location
  template_name = 'location/delete.html'
  success_url = reverse_lazy('sh:location_list')

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
        context['page_title'] = 'Localidades'
        context['title'] = 'Eliminar una Localidad'
        context['del_title'] = 'Localidad: '
        context['list_url'] = reverse_lazy('sh:location_list')
        context['form_id'] = 'locationForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context