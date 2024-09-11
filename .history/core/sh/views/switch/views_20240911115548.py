from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import SwitchForm
from core.sh.models import Dev_Model, Edifice, Office, Switch

class SwitchListView(ListView):
  model = Switch
  template_name = 'switch/list.html'

  @method_decorator(login_required)
  @method_decorator(csrf_exempt)
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
  model: Switch
  form_class = SwitchForm
  template_name = 'switch/create.html'
  success_url = reverse_lazy('sh:switch_list')

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

        elif action == 'search_edifice':
          location_id = request.POST.get('location_id')
          edifices = Edifice.objects.filter(location_id=location_id)
          data = [{'id':e.id, 'name': e.edifice} for e in edifices]

        elif action == 'search_office':
          edifice_id = request.POST.get('edifice_id')
          offices = Office.objects.filter(edifice_id=edifice_id)
          data = [{'id': o.id, 'name': o.wall_port} for o in offices]

        else:
          form = SwitchForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Switch guardado correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar el Switch: {str(e)}"}, status=400)
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
    context['page_title'] = 'Switchs'
    context['title'] = 'Agregar una Switch'
    context['btn_add_id'] = 'switch_add'
    context['entity'] = 'Switchs'
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['form_id'] = 'switchForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class SwitchUpadateView(UpdateView):
  model = Switch
  form_class = SwitchForm
  template_name = 'switch/create.html'
  success_url = reverse_lazy('sh:switch_list')

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

        elif action == 'search_edifice':
          location_id = request.POST.get('location_id')
          edifices = Edifice.objects.filter(location_id=location_id)
          data = [{'id':e.id, 'name': e.edifice} for e in edifices]

        elif action == 'search_office':
          edifice_id = request.POST.get('edifice_id')
          offices = Office.objects.filter(edifice_id=edifice_id)
          data = [{'id': o.id, 'name': o.wall_port} for o in offices]

        else:
          self.object = self.get_object()
          form = self.get_form()
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Switch actualizado correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error": f"Error al actualizar el Switch: {str(e)}"}, status=400)
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
      if brand_id:
        try:
          brand_id = int(brand_id)
          models = models.filter(brand_id=brand_id)
        except ValueError:
          pass
        data = [{'id': m.id, 'name': m.dev_model} for m in models]

      elif action == 'search_edifice':
        location_id = post_data.get('location_id')
        if location_id:
          try:
            location_id = int(location_id)
            edifices = Edifice.objects.filter(location_id=location_id)
            data = [{'id':e.id, 'name': e.edifice} for e in edifices]
          except ValueError:
            pass

      elif action == 'search_office':
        edifice_id = post_data.get('edifice_id')
        if edifice_id:
          try:
            edifice_id = int(edifice_id)
            offices = Office.objects.filter(edifice_id=edifice_id)
            data = [{'id': o.id, 'name': o.office} for o in offices]
          except ValueError:
            pass

      return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Switchs '
    context['title'] = 'Editar un Switch'
    context['btn_add_id'] = 'switch_add'
    context['entity'] = 'Switchs'
    context['list_url'] = reverse_lazy('sh:switch_list')
    context['form_id'] = 'switchForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    switch = self.get_object()

    context['form'].fields['model'].queryset = Dev_Model.objects.filter(
      dev_type = switch.model.dev_type,
      brand = switch.model.brand
    )
    context['form'].fields['edifice'].queryset = Edifice.objects.filter(
      location = switch.office.edifice.location
    )
    context['form'].fields['office'].queryset = Office.objects.filter(
      office = switch.office.edifice
    )

    context['form'].initial['brand'] = switch.model.brand.id if switch.model.brand else None
    context['form'].initial['dev_type'] = switch.model.dev_type.id if switch.model.dev_type else 'SWITCH'
    context['form'].initial['model'] = switch.model.id if switch.model else None
    context['form'].initial['location'] = switch.office.edifice.location.id if switch.office.edifice.location else None
    context['form'].initial['edifice'] = switch.office.edifice.id if switch.office.edifice else None
    context['form'].initial['office'] = switch.office.id if switch.office else None

    context['form'].fields['model'].widget.attrs.update({
      'data-preselected': self.object.model.id if self.object.model else ''
    })
    context['form'].fields['edifice'].widget.attrs.update({
      'data-preselected': self.object.office.edifice.id if self.object.office.edifice else ''
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