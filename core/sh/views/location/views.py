from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import LocationForm
from core.sh.forms.modals.forms import ProvinceModalForm
from core.sh.models import Location


class LocationListView(ListView):
  model = Location
  template_name = 'location/list.html'

  @method_decorator(login_required)
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for l in Location.objects.all():
          data.append(l.toJSON())
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
    context['add_btn_title'] = 'Agregar Localidad'
    return context

class LocationCreateView(CreateView):
  model: Location
  form_class = LocationForm
  template_name = 'location/create.html'
  success_url = reverse_lazy('sh:location_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def get_template_names(self):
    if self.request.GET.get('popup') == '1':
      return ['location/popup_add.html']
    return ['location/create.html']

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Localidad creada exitosamente',
          'location_id': self.object.id,
          'location_name': self.object.location,
          'province_id': self.object.province.id,
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
    context['page_title'] = 'Localidades'
    context['title'] = 'Agregar una Localidad'
    context['btn_add_id'] = 'location_add'
    context['entity'] = 'Localidades'
    context['list_url'] = reverse_lazy('sh:location_list')
    context['form_id'] = 'locationForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-custom-primary'
    context['btn_color'] = 'btn-primary'
    context['province_modal_add'] = ProvinceModalForm()
    context['saved'] = kwargs.get('saved', None)
    return context

class LocationUpadateView(UpdateView):
  model = Location
  form_class = LocationForm
  template_name = 'location/create.html'
  success_url = reverse_lazy('sh:location_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Localidad actualizada correctamente',
          'location_id': self.object.id,
          'location_name': self.object.location,
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
    context['page_title'] = 'Localidades'
    context['title'] = 'Editar Localidad'
    context['btn_add_id'] = 'location_add'
    context['entity'] = 'Localidades'
    context['list_url'] = reverse_lazy('sh:location_list')
    context['form_id'] = 'locationForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-custom-warning'
    context['btn_color'] = 'bg-custom-warning'
    context['province_modal_add'] = ProvinceModalForm()
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
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context