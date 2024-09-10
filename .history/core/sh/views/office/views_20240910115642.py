from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import OfficeForm
from core.sh.models import Dependency, Edifice, Office, Office_Loc


class OfficeListView(ListView):
  model = Office
  template_name = 'office/list.html'

  # @method_decorator(login_required)
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Office.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
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

  def post(self, request, *args, **kwargs):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')
        if action == 'search_dependency':
          location_id = request.POST.get('location_id')

          dependencyes = Dependency.objects.all()
          if location_id:
            dependencyes = dependencyes.filter(location_id=location_id)

          data = [{'id': d.id, 'name': d.dependency} for d in dependencyes]

        elif action == 'search_edifice':
          edifices = Edifice.objects.filter(location_id=location_id)
          data = [{'id':e.id, 'name': e.edifice} for e in edifices]

        elif action == 'search_loc':
          edifice_id = request.POST.get('edifice_id')
          office_locs = Office_Loc.objects.filter(edifice_id=edifice_id)
          data = [{'id': ol.id, 'name': str({{ol.floor}} + '/' + {{ol.wing}})} for ol in office_locs]

        else:
          form = OfficeForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Oficina guardada correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar la Oficina: {str(e)}"}, status=400)
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
    context['page_title'] = 'Oficinas'
    context['title'] = 'Agregar una Oficina'
    context['btn_add_id'] = 'office_add'
    context['entity'] = 'Oficinas'
    context['list_url'] = reverse_lazy('sh:office_list')
    context['form_id'] = 'officeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class OfficeUpadateView(UpdateView):
  model = Office
  form_class = OfficeForm
  template_name = 'office/create.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
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
      context['page_title'] = 'Oficinas'
      context['title'] = 'Editar Oficina'
      context['btn_add_id'] = 'office_add'
      context['entity'] = 'Oficinas'
      context['list_url'] = reverse_lazy('sh:office_list')
      context['form_id'] = 'officeForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
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