from django.contrib.auth.decorators import login_required
from django.forms import BaseModelForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import OfficeLocForm
from core.sh.models import Edifice, Location, Office_Loc


class OfficeLocListView(ListView):
  model = Office_Loc
  template_name = 'office_loc/list.html'

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
        for i in Office_Loc.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Locacion de Oficinas ( Piso / Ala )'
    context['title'] = 'Listado de Locaciones de Oficinas'
    context['btn_add_id'] = 'office_loc_add'
    context['create_url'] = reverse_lazy('sh:office_loc_add')
    context['list_url'] = reverse_lazy('sh:office_loc_list')
    context['entity'] = 'Locacion de Oficinas'
    context['nav_icon'] = 'fa-regular fa-building'
    context['table_id'] = 'office_loc_table'
    return context

class OfficeLocCreateView(CreateView):
  model: Office_Loc
  form_class = OfficeLocForm
  template_name = 'office_loc/create.html'
  success_url = reverse_lazy('sh:office_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')
        if action == 'search_location':
          province_id = request.POST.get('province_id')

          locations = Location.objects.all()
          if province_id:
            locations = locations.filter(province_id=province_id)

          data = [{'id': l.id, 'name': l.location} for l in locations]

        elif action == 'search_edifice':
          location_id = request.POST.get('location_id')

          edifices = Edifice.objects.all()
          if location_id:
            edifices = edifices.filter(location_id=location_id)

          data = [{'id': e.id, 'name': e.edifice} for e in edifices]

        else:
          form = OfficeLocForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Locación de Oficina agregada corectamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar la locación de edificio: {str(e)}"}, status=400)
          else:
            errors = form.errors.get_json_data()
            return JsonResponse({"error": "Formulario no válido", "form_errors":errors}, status=400)

        return JsonResponse(data, safe=False)

      except Exception as e:
        return JsonResponse({'error': str(e)}, status=400, safe=False)

    else:
      return super().post(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Locacion de Oficinas ( Piso / Ala )'
    context['title'] = 'Agregar una Locacion de Oficina ( Piso / Ala )'
    context['btn_add_id'] = 'office_loc_add'
    context['entity'] = 'Locaciond de Oficinas'
    context['list_url'] = reverse_lazy('sh:office_loc_list')
    context['form_id'] = 'officeLocForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class OfficeLocUpadateView(UpdateView):
  model = Office_Loc
  form_class = OfficeLocForm
  template_name = 'office_loc/create.html'
  success_url = reverse_lazy('sh:office_loc_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')
        if action == 'search_location':
          province_id = request.POST.get('province_id')

          locations = Location.objects.all()
          if province_id:
            locations = locations.filter(province_id=province_id)

          data = [{'id': l.id, 'name': l.location} for l in locations]

        elif action == 'search_edifice':
          location_id = request.POST.get('location_id')

          edifices = Edifice.objects.all()
          if location_id:
            edifices = edifices.filter(location_id=location_id)

          data = [{'id': e.id, 'name': e.edifice} for e in edifices]

        else:
          form = OfficeLocForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Locación de Oficina agregada corectamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar la locación de edificio: {str(e)}"}, status=400)
          else:
            errors = form.errors.get_json_data()
            return JsonResponse({"error": "Formulario no válido", "form_errors":errors}, status=400)

        return JsonResponse(data, safe=False)

      except Exception as e:
        return JsonResponse({'error': str(e)}, status=400, safe=False)

    else:
      return super().post(request, *args, **kwargs)

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

  def handle_search_action(self, action, post_data):

    data = []

    if action == 'search_location':
      province_id = post_data.get('province_id')
      locations = Location.objects.all()
      if province_id:
        try:
          province_id = int(province_id)
          locations = locations.filter(province_id=province_id)
          data = [{'id': l.id, 'name': l.location} for l in locations]
        except ValueError:
          pass
      else:
        data = {'Error': 'No se proporcionó un ID de provincia válido'}

    elif action ==  'search_edifice':
      location_id = post_data.get('location_id')
      edifices = Edifice.objects.all()
      if location_id:
        try:
          location_id = int(location_id)
          edifices = edifices.filter(location_id=location_id)
          data = [{'id': e.id, 'name': e.edifices} for e in edifices]
        except ValueError:
          pass
      else:
        data = {'Error': 'No se proporcionó un ID de Localidad válido'}

    return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Locación de Oficinas ( Piso / Ala)'
    context['title'] = 'Editar Locación de Oficina ( Piso / Ala)'
    context['btn_add_id'] = 'office_loc_add'
    context['entity'] = 'Locacion de Oficinas'
    context['list_url'] = reverse_lazy('sh:office_loc_list')
    context['form_id'] = 'officeLocForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    office_loc = self.get_object()

    context['form'].fields['location'].queryset = Location.objects.filter(
      province = office_loc.edifice.location.province
    )
    context['form'].fields['edifice'].queryset =  Edifice.objects.filter(
      location = office_loc.edifice.location
    )

    context['form'].initial['province'] = office_loc.edifice.location.province.id if office_loc.edifice.location.province else None

    context['form'].fields['location'].widget.attrs.update({
      'data-preselected': self.object.edificie.id if self.object.edifice else ''
    })
    context['form'].fields['edifice'].widget.attrs.update({
      'data-preselected': self.object.edifice.id if self.object.edifice else ''
    })


    return context

class OfficeLocDeleteView(DeleteView):
  model = Office_Loc
  template_name = 'office_loc/delete.html'
  success_url = reverse_lazy('sh:office_loc_list')

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
        context['page_title'] = 'Locacion de Oficinas ( Piso / Ala )'
        context['title'] = 'Eliminar una Locacion de Oficina ( Piso / Ala )'
        context['del_title'] = 'Locacion de Oficina: '
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['form_id'] = 'officeLocForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context