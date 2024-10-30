from django.contrib.auth.decorators import login_required 
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms import DeviceForm
from core.sh.models import Device, Dev_Model, Employee, Office, Switch_Port, Wall_Port
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province

#Ajax Views

@csrf_protect
def ajax_device_search_location(request):
  data=[]
  if request.method == 'POST':
    province_id = request.POST.get('province_id')
    locations = Location.objects.filter(province_id=province_id)
    data = [{'id': l.id, 'name': l.location} for l in locations]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_dependency(request):
  data=[]
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    dependencies = Dependency.objects.filter(edifice__location_id=location_id)
    data = [{'id': d.id, 'name': d.dependency} for d in dependencies]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_edifices(request):
  data=[]
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    edifices = Edifice.objects.filter(location_id=location_id)
    data = [{'id': e.id, 'name': e.edifice} for e in edifices]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_loc(request):
  data = []
  if request.method == 'POST':
    edifice_id = request.POST.get('edifice_id')
    locs = Office_Loc.objects.filter(edifice_id=edifice_id)
    data = [{'id': fw.id, 'name': f'Piso: {fw.floor} / Ala: {fw.wing}'} for fw in locs]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_office(request):
  data=[]
  if request.method == 'POST':
    loc_id = request.POST.get('loc_id')
    offices = Office.objects.filter(loc_id=loc_id)
    data = [{'id': o.id, 'name': o.office} for o in offices]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_wall_port(request):
  data=[]
  if request.method == 'POST':
    office_id = request.POST.get('office_id')
    wall_ports = Wall_Port.objects.filter(office_id=office_id)
    data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_switch_port(request):
  data=[]
  if request.method == 'POST':
    office_id = request.POST.get('office_id')
    switch_ports = Switch_Port.objects.filter(switch__office_id=office_id)
    data = [{'id': s.id, 'name': f'Puerto: {s.port_id}, Switch: {s.switch}'} for s in switch_ports]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_employee(request):
  data=[]
  if request.method == 'POST':
    office_id = request.POST.get('office_id')
    employees = Employee.objects.filter(office_id=office_id)
    data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_device_load_model(request):
  data=[]
  if request.method == 'POST':
    brand_id = request.POST.get('brand_id')
    dev_type_id = request.POST.get('dev_type_id')
    models = Dev_Model.objects.filter(brand_id=brand_id, dev_type_id=dev_type_id)
    data = [{'id': m.id, 'name': m.dev_model} for m in models]
  return JsonResponse(data, safe=False)

class DeviceListView(ListView):
  model = Device
  template_name = 'device/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST.get('action')
      if action == 'searchdata':
        devices = Device.objects.all()
        data = [d.toJSON() for d in devices]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Dispositivos'
    context['title'] = 'Listado de Dispositivos'
    context['btn_add_id'] = 'device_add'
    context['create_url'] = reverse_lazy('sh:device_add')
    context['list_url'] = reverse_lazy('sh:device_list')
    context['entity'] = 'Dispositivos'
    context['nav_icon'] = 'fa-solid fa-ethernet'
    context['table_id'] = 'device_table'
    return context

class DeviceCreateView(CreateView):
  model = Device
  form_class = DeviceForm
  template_name = "device/create.html"
  success_url = reverse_lazy('sh:device_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Dispositivo agregado correctamente'
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
    context['page_title'] = 'Dispositivos'
    context['title'] = 'Agregar un Dispositivo'
    context['btn_add_id'] = 'device_add'
    context['entity'] = 'Dispositivos'
    context['list_url'] = reverse_lazy('sh:device_list')
    context['form_id'] = 'deviceForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class DeviceUpdateView(UpdateView):
  model = Device
  form_class = DeviceForm
  template_name = 'device/create.html'
  success_url = reverse_lazy('sh:device_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Dispositivo actualizado correctamente'
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
    context['page_title'] = 'Dispositivos'
    context['title'] = 'Editar Dispositivo'
    context['btn_add_id'] = 'device_add'
    context['entity'] = 'Dispositivos'
    context['list_url'] = reverse_lazy('sh:device_list')
    context['form_id'] = 'deviceForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    device = self.get_object()

    if device.office and device.office.loc and device.office.loc.edifice and device.office.loc.edifice.location and device.office.loc.edifice.location.province and device.office.dependency:

      province = device.office.loc.edifice.location.province
      context['form'].fields['province'].queryset = Province.objects.all()
      context['form'].fields['province'] = province.id

      location = device.office.loc.edifice.location
      context['form'].fields['location'].queryset = Location.objects.filter(province=province)
      context['form'].initial['location'] = location.id

      edifice = device.office.loc.edifice
      context['form'].fields['edifice'].queryset = Edifice.objects.filter(location=location)
      context['form'].initial['edifice'] = edifice.id

      dependency = device.office.dependency
      context['form'].fields['dependency'].queryset = Dependency.objects.filter(edifice__location=location)
      context['form'].initial['dependency'] = dependency.id

      loc = device.office.loc
      context['form'].fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
      context['form'].initial['loc'] = loc.id

      office = device.office
      context['form'].fields['office'].queryset = Office.objects.filter(loc=loc)
      context['form'].initial['office'] = office.id

      wall_port = device.wall_port
      context['form'].fields['wall_port'].queryset = Wall_Port.objects.filter(office=office)
      context['form'].initial['wall_port'] = wall_port

      context['form'].fields['employee'].queryset = Employee.objects.filter(office=office)
      employees = device.employee.all()
      context['form'].initial['employee'] = [e.id for e in employees]

      switch_port = device.switch_port
      context['form'].fields['switch_port'].queryset = Switch_Port.objects.filter(switch__office=office)
      context['form'].initial['switch_port'] = switch_port

    return context

class DeviceDeleteView(DeleteView):
  model = Device
  template_name = 'device/delete.html'
  success_url = reverse_lazy('sh:device_list')

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
    context['page_title'] = 'Dispositivos'
    context['title'] = 'Eliminar un Dispositivo'
    context['del_title'] = 'Dispositivo: '
    context['list_url'] = reverse_lazy('sh:device_list')
    context['form_id'] = 'deviceForm'
    context['bg_color'] = 'bg-danger'
    context['action'] = 'delete'
    return context