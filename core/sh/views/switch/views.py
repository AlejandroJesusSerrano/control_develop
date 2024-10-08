from django.contrib.auth.decorators import login_required 
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms.switch.forms import SwitchForm
from core.sh.models import Brand, Dependency, Dev_Model, Dev_Type, Edifice, Office, Switch, Location

# Ajax views

@csrf_protect
def ajax_switch_search_brand(request):
  data=[]
  if request.method == 'POST':
    dev_type_name = request.POST.get('dev_type_name', 'SWITCH')
    try:
      dev_type = Dev_Type.objects.get(dev_type=dev_type_name)
      brands = Brand.objects.filter(models_brand__dev_type__dev_type=dev_type_name).distinct()
      data = [{'id': b.id, 'name': b.brand}for b in brands]
    except Dev_Type.DoesNotExist:
      pass
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_switch_search_model(request):
  data = []
  if request.method == 'POST':
    brand_id = request.POST.get('brand_id')
    dev_type_id = request.POST.get('dev_type_id')
    models = Dev_Model.objects.filter(dev_type__dev_type='SWITCH')
    if brand_id:
      models = models.filter(brand_id=brand_id)
    data = [{'id': m.id, 'name': m.dev_model} for m in models]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_switch_search_location(request):
  data = []
  if request.method == 'POST':
    province_id = request.POST.get('province_id')
    locations = Location.objects.filter(province_id=province_id)
    data = [{'id': l.id, 'name': l.location} for l in locations]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_switch_search_edifice(request):
  data = []
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    edifices = Edifice.objects.filter(location_id=location_id)
    data = [{'id': e.id, 'name': e.edifice} for e in edifices]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_switch_search_dependency(request):
  data = []
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    dependencies = Dependency.objects.filter(edifice__location_id=location_id)
    data = [{'id': d.id, 'name': d.dependency} for d in dependencies]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_switch_search_office(request):
  data = []
  if request.method == 'POST':
    edifice_id = request.POST.get('edifice_id')
    dependency_id = request.POST.get('dependency_id')
    offices = Office.objects.all()
    if edifice_id:
      offices = offices.filter(loc__edifice_id=edifice_id)
    if dependency_id:
      offices = offices.filter(dependency_id=dependency_id)
    data = [{'id': o.id, 'name': o.office} for o in offices]
  return JsonResponse(data, safe=False)

class SwitchListView(ListView):
  model = Switch
  template_name = 'switch/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        switches = Switch.objects.all()
        data = [s.toJSON() for s in switches]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Switchs'
    context['title'] = 'Listado de Switchs'
    context['btn_add_id'] = 'switch_add'
    context['create_url'] = reverse_lazy('sh:switch_add')
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['entity'] = 'Switchs'
    context['nav_icon'] = 'fa fa-copyright'
    context['table_id'] = 'switch_table'
    return context

class SwitchCreateView(CreateView):
  model = Switch
  form_class = SwitchForm
  template_name = 'switch/create.html'
  success_url = reverse_lazy('sh:switch_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Switch agregado exitosamente',
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
    context['page_title'] = 'Switchs'
    context['title'] = 'Agregar una Switch'
    context['btn_add_id'] = 'switch_add'
    context['entity'] = 'Switchs'
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['form_id'] = 'switchForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    context['dev_type_id'] = 'SWITCH'
    return context

class SwitchUpdateView(UpdateView):
  model = Switch
  form_class = SwitchForm
  template_name = 'switch/create.html'
  success_url = reverse_lazy('sh:switch_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Switch actualizado exitosamente',
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
    context['page_title'] = 'Switchs'
    context['title'] = 'Editar un Switch'
    context['btn_add_id'] = 'switch_add'
    context['entity'] = 'Switchs'
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['form_id'] = 'switchForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    switch = self.get_object()

    if switch.model:
      context['form'].fields['brand'].queryset = Brand.objects.filter(
        models_brand__dev_type=switch.model.dev_type
      ).distinct()

      context['form'].fields['model'].queryset = Dev_Model.objects.filter(
        dev_type=switch.model.dev_type,
        brand=switch.model.brand
    )

    if switch.office and switch.office.loc and switch.office.loc.edifice:
      context['form'].fields['edifice'].queryset = Edifice.objects.filter(
        location=switch.office.loc.edifice.location
    )

    if switch.office:
      context['form'].fields['office'].queryset = Office.objects.select_related('loc__edifice').filter(
        loc__edifice=switch.office.loc.edifice
    )

# Manejar inicialización segura de datos en el contexto
    context['form'].initial['brand'] = switch.model.brand.id if switch.model and switch.model.brand else None
    context['form'].initial['dev_type'] = switch.model.dev_type.id if switch.model and switch.model.dev_type else 'SWITCH'
    context['form'].initial['model'] = switch.model.id if switch.model else None

    if switch.office and switch.office.loc and switch.office.loc.edifice:
      context['form'].initial['location'] = switch.office.loc.edifice.location.id
      context['form'].initial['edifice'] = switch.office.loc.edifice.id
      context['form'].initial['office'] = switch.office.id if switch.office else None

    context['form'].fields['brand'].widget.attrs.update({
      'data-preselected': self.object.model.brand.id if self.object.model and self.object.model.brand else ''
    })
    context['form'].fields['model'].widget.attrs.update({
      'data-preselected': self.object.model.id if self.object.model else ''
    })
    context['form'].fields['edifice'].widget.attrs.update({
      'data-preselected': self.object.office.loc.edifice.id if self.object.office.loc.edifice else ''
    })
    context['form'].fields['office'].widget.attrs.update({
      'data-preselected': self.object.office.id if self.object.office else ''
    })

    return context

class SwitchDeleteView(DeleteView):
  model = Switch
  template_name = 'switch/delete.html'
  success_url = reverse_lazy('sh:switch_list')

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
        context['page_title'] = 'Switchs'
        context['title'] = 'Eliminar un Switch'
        context['del_title'] = 'Switch: '
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['form_id'] = 'switchForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context