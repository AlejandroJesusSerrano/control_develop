from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms import OfficeForm
from core.sh.models import Dependency, Edifice, Location, Office, Office_Loc, Province

# Ajax View
@csrf_protect
def ajax_office_search_location(request):
  data = []
  if request.method == 'POST':
    province_id = request.POST.get('province_id')
    locations = Location.objects.filter(province_id=province_id)
    data = [{'id': l.id, 'name': l.location} for l in locations]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_dependency(request):
  data = []
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    dependencies = Dependency.objects.filter(edifice__location_id=location_id)
    data = [{'id': d.id, 'name': d.dependency} for d in dependencies]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_edifices(request):
  data = []
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    edifices = Edifice.objects.filter(location_id=location_id)
    data = [{'id': e.id, 'name': e.edifice} for e in edifices]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_loc(request):
  data = []
  if request.method == 'POST':
    edifice_id = request.POST.get('edifice_id')
    locs = Office_Loc.objects.filter(edifice_id=edifice_id)
    data = [{'id': fw.id, 'name': f'Piso: {fw.floor} / Ala: {fw.wing}'} for fw in locs]
  return JsonResponse(data, safe=False)

class OfficeListView(ListView):
  model = Office
  template_name = 'office/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST.get('action')
      if action == 'searchdata':
        offices = Office.objects.all()
        data = [o.toJSON() for o in offices]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Oficinas'
    context['title'] = 'Listado de Oficinas'
    context['btn_add_id'] = 'office_add'
    context['create_url'] = reverse_lazy('sh:office_add')
    context['list_url'] = reverse_lazy('sh:office_list')
    context['entity'] = 'Oficinas'
    context['nav_icon'] = 'fa-regular fa-building'
    context['table_id'] = 'office_table'
    return context

class OfficeCreateView(CreateView):
  model: Office
  form_class = OfficeForm
  template_name = 'office/create.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Oficina agregada correctamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-reuquested-with') == 'XMLHttpRequest':
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
    context['page_title'] = 'Oficinas'
    context['title'] = 'Agregar una Oficina'
    context['btn_add_id'] = 'office_add'
    context['entity'] = 'Oficinas'
    context['list_url'] = reverse_lazy('sh:office_list')
    context['form_id'] = 'officeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class OfficeUpdateView(UpdateView):
  model = Office
  form_class = OfficeForm
  template_name = 'office/create.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Oficina actualizada correctamente'
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
      return JsonResponse({'error':errors}, status=400)
    else:
      return super().form_invalid(form)


  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Oficinas'
      context['title'] = 'Editar Oficina'
      context['btn_add_id'] = 'office_add'
      context['entity'] = 'Oficinas'
      context['list_url'] = reverse_lazy('sh:office_list')
      context['form_id'] = 'officeForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'

      office = self.get_object()

      if office.loc and office.loc.edifice and office.loc.edifice.location and office.loc.edifice.location.province and office.dependency:

        province = office.loc.edifice.location.province
        context['form'].fields['province'].queryset = Province.objects.all()
        context['form'].initial['province'] = province.id

        location = office.loc.edifice.location
        context['form'].fields['location'].queryset = Location.objects.filter(province=province)
        context['form'].initial['location'] = location.id

        edifice = office.loc.edifice
        context['form'].fields['edifice'].queryset = Edifice.objects.filter(location=location)
        context['form'].initial['edifice'] = edifice.id

        dependency = office.dependency
        context['form'].fields['dependency'].queryset = Dependency.objects.filter(edifice__location=location)
        context['form'].initial['dependency'] = dependency.id

        wing_floor = office.loc
        context['form'].fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
        context['form'].initial['loc'] = wing_floor.id

      return context

class OfficeDeleteView(DeleteView):
  model = Office
  template_name = 'office/delete.html'
  success_url = reverse_lazy('sh:office_list')

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
        context['page_title'] = 'Oficinas'
        context['title'] = 'Eliminar una Oficina'
        context['del_title'] = 'Oficina: '
        context['list_url'] = reverse_lazy('sh:office_list')
        context['form_id'] = 'officeForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context