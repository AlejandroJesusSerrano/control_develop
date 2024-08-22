from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import DeviceForm
from core.sh.models import Device, Dev_Model, Employee, Switch_Port, Wall_Port

class DeviceListView(ListView):
  model = Device
  template_name = 'device/list.html'

  @method_decorator(login_required)
  @method_decorator(csrf_exempt)
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

class DeviceCreateView(TemplateView):
    template_name = "device/create.html"

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {}
        try:
          action = request.POST.get('action')
          if action == 'search_models':
            dev_type_id = request.POST.get('dev_type_id')
            brand_id = request.POST.get('brand_id')

            models = Dev_Model.objects.all()
            if dev_type_id:
              models = models.filter(dev_type_id=dev_type_id)
            if brand_id:
              models = models.filter(brand_id=brand_id)

            data = [{'id':m.id, 'name':m.dev_model}for m in models]

          elif action == 'search_wall_ports':
            office_id = request.POST.get('office_id')

            wall_ports = Wall_Port.objects.filter(office_id = office_id)
            data = [{'id': w.id, 'name':w.wall_port}for w in wall_ports]

          elif action == 'search_switch_ports':
            office_id = request.POST.get('office_id')

            switch_ports = Switch_Port.objects.filter(office_id = office_id)
            data = [{'id': s.id, 'name':s.port_id}for s in switch_ports]

          elif action == 'search_employees':
            office_id = request.POST.get('office_id')

            employees = Employee.objects.filter(office_id = office_id)
            data = [{'id': e.id, 'name':f'{e.employee_last_name}, {e.employee_name}'}for e in employees]

          else:
            data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data, safe=False)

      else:
        form = DeviceForm(request.POST)
        if form.is_valid():
          form.save()
          return HttpResponseRedirect(reverse_lazy('sh:device_list'))
        else:
          context = self.get_context_data(**kwargs)
          context['form'] = form
          return self.render_to_response(context)

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
      context['form'] = DeviceForm()
      return context

# class DeviceCreateView(CreateView):
#   model: Device
#   form_class = DeviceForm
#   template_name = 'device/create.html'
#   success_url = reverse_lazy('sh:device_list')

#   @method_decorator(login_required)
#   def dispatch(self, request, *args, **kwargs):
#     return super().dispatch(request, *args, **kwargs)

#   def post(self, request, *args, **kwargs):
#     data={}
#     try:
#       action = request.POST.get('action')
#       if action == 'add':
#         form = self.get_form()
#         data = form.save()
#       else:
#         data['error'] = 'Acción no válida'
#     except Exception as e:
#       data['error'] = str(e)
#     return JsonResponse(data)

#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['page_title'] = 'Dispositivos'
#     context['title'] = 'Agregar un Dispositivo'
#     context['btn_add_id'] = 'device_add'
#     context['entity'] = 'Dispositivos'
#     context['list_url'] = reverse_lazy('sh:device_list')
#     context['form_id'] = 'deviceForm'
#     context['action'] = 'add'
#     context['bg_color'] = 'bg-primary'
#     context['form'] = DeviceForm()
#     return context

class DeviceUpadateView(UpdateView):
  model = Device
  form_class = DeviceForm
  template_name = 'device/create.html'
  success_url = reverse_lazy('sh:device_list')

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
      context['page_title'] = 'Dispositivos'
      context['title'] = 'Editar el Nombre de un Dispositivo'
      context['btn_add_id'] = 'device_add'
      context['entity'] = 'Dispositivos'
      context['list_url'] = reverse_lazy('sh:device_list')
      context['form_id'] = 'deviceForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
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