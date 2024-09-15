from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import DeviceForm
from core.sh.models import Device, Dev_Model, Employee, Office, Switch_Port, Wall_Port

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

class DeviceCreateView(CreateView):
  model = Device
  form_class = DeviceForm
  template_name = "device/create.html"
  success_url = reverse_lazy('sh:device_list')

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)

  def post(self, request, *args, **kwargs):
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

          data = [{'id': m.id, 'name': m.dev_model} for m in models]

        elif action == 'search_office':
          dependency_id = request.POST.get('dependency_id')
          office = Office.objects.filter(dependency_id=dependency_id)
          data = [{'id':o.id, 'name': o.office} for o in office]

        elif action == 'search_wall_ports':
          office_id = request.POST.get('office_id')
          wall_ports = Wall_Port.objects.filter(office_id=office_id)
          data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]

        elif action == 'search_switch_ports':
          office_id = request.POST.get('office_id')
          switch_ports = Switch_Port.objects.filter(switch__office_id=office_id)
          data = [{'id': s.id, 'name': s.port_id} for s in switch_ports]

        elif action == 'search_employees':
          office_id = request.POST.get('office_id')
          employees = Employee.objects.filter(office_id=office_id)
          data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]

        else:
          form = DeviceForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Dispositivo guardado correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar el dispositivo: {str(e)}"}, status=400)
          else:
            errors = form.errors.get_json_data()
            return JsonResponse({"error": "Formulario no valido", "form_errors":errors}, status=400)

        return JsonResponse(data, safe=False)

      except Exception as e:
        return JsonResponse({'error': str(e)}, status=400, safe=False)

    else:
      return super().post(request, *args, **kwargs)

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

  def post(self, request, *args, **kwargs):
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

          data = [{'id': m.id, 'name': m.dev_model} for m in models]

        elif action == 'search_office':
          dependency_id = request.POST.get('dependency_id')
          office = Office.objects.filter(dependency_id=dependency_id)
          data = [{'id':o.id, 'name': o.office} for o in office]

        elif action == 'search_wall_ports':
          office_id = request.POST.get('office_id')
          wall_ports = Wall_Port.objects.filter(office_id=office_id)
          data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]

        elif action == 'search_switch_ports':
          office_id = request.POST.get('office_id')
          switch_ports = Switch_Port.objects.filter(switch__office_id=office_id)
          data = [{'id': s.id, 'name': s.port_id} for s in switch_ports]

        elif action == 'search_employees':
          office_id = request.POST.get('office_id')
          employees = Employee.objects.filter(office_id=office_id)
          data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]

        else:
          self.object = self.get_object()
          form = self.get_form()  # Se ha añadido para obtener el formulario con la instancia actual
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Dispositivo actualizado correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error": f"Error al guardar el dispositivo: {str(e)}"}, status=400)
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

    if action =='search_models':
      dev_type_id = post_data.get('dev_type_id')
      brand_id = post_data.get('brand_id')
      models = Dev_Model.objects.all()
      if dev_type_id:
        try:
          dev_type_id = int(dev_type_id)
          models = models.filter(dev_type_id=dev_type_id)
        except ValueError:
          pass
          # models = models.filter(dev_type_id=dev_type_id)

      if brand_id:
        try:
          brand_id = int(brand_id)
          models = models.filter(brand_id=brand_id)
        except ValueError:
          pass
        data = [{'id': m.id, 'name': m.dev_model} for m in models]

    elif action == 'search_office':
      dependency_id = post_data.get('dependency_id')
      if dependency_id:
        try:
          dependency_id = int(dependency_id)
          office = Office.objects.filter(dependency_id=dependency_id)
          data = [{'id':o.id, 'name': o.office} for o in office]
        except ValueError:
          pass

    elif action == 'search_wall_ports':
      office_id = post_data.get('office_id')
      if office_id:
        try:
          office_id = int(office_id)
          wall_ports = Wall_Port.objects.filter(office_id=office_id)
          data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]
        except ValueError:
          pass

    elif action == 'search_switch_ports':
      office_id = post_data.get('office_id')
      if office_id:
        try:
          office_id = int(office_id)
          switch_ports = Switch_Port.objects.filter(switch__office_id=office_id)
          data = [{'id': s.id, 'name': s.port_id} for s in switch_ports]
        except ValueError:
          pass

    elif action == 'search_employees':
      office_id = post_data.get('office_id')
      if office_id:
        try:
          office_id = int(office_id)
          employees = Employee.objects.filter(office_id=office_id)
          data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]
        except ValueError:
          pass

    return data

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

    context['form'].fields['office'].queryset = Office.objects.filter(
      dependency = device.office.dependency
    )

    context['form'].fields['dev_model'].queryset = Dev_Model.objects.filter(
        brand=device.dev_model.brand,
        dev_type=device.dev_model.dev_type
        )

    context['form'].fields['wall_port'].queryset = Wall_Port.objects.filter(
        office=device.office
    )

    context['form'].fields['switch_port'].queryset = Switch_Port.objects.filter(
        switch__office=device.office
    )

    context['form'].fields['employee'].queryset = Employee.objects.filter(
        office=device.office
    )

    context['form'].initial['dev_type'] = device.dev_model.dev_type.id if device.dev_model.dev_type else None
    context['form'].initial['brand'] = device.dev_model.brand.id if device.dev_model.brand else None
    context['form'].initial['dev_model'] = device.dev_model.id if device.dev_model else None
    context['form'].initial['dependency'] = device.office.dependency.id if device.office.dependency else None
    context['form'].initial['office'] = device.office.id if device.office else None
    context['form'].initial['wall_port'] = device.wall_port.id if device.wall_port else None
    context['form'].initial['switch_port'] = device.switch_port.id if device.switch_port else None
    context['form'].initial['employee'] = [emp.id for emp in device.employee.all()] if device.employee.exists() else None

    context['form'].fields['dev_model'].widget.attrs.update({
      'data-preselected': self.object.dev_model.id if self.object.dev_model else ''
    })
    context['form'].fields['office'].widget.attrs.update({
      'data-preselected': self.object.office.id if self.object.office else ''
    })
    context['form'].fields['wall_port'].widget.attrs.update({
      'data-preselected': self.object.wall_port.id if self.object.wall_port else ''
    })
    context['form'].fields['switch_port'].widget.attrs.update({
      'data-preselected': self.object.switch_port.id if self.object.switch_port else ''
    })
    context['form'].fields['employee'].widget.attrs.update({
      'data-preselected': [emp.id for emp in self.object.employee.all()] if self.object.employee.exists() else ''
    })

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