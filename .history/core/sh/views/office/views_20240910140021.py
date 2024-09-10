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

          dependencies = Dependency.objects.all()
          if location_id:
            dependencies = dependencies.filter(location_id=location_id)

          data = [{'id': d.id, 'name': d.dependency} for d in dependencies]

        elif action == 'search_edifice':
          location_id = request.POST.get('location_id')
          if location_id:
            edifices = Edifice.objects.filter(location_id=location_id)
            data = [{'id':e.id, 'name': e.edifice} for e in edifices]
          else:
            data = []

        elif action == 'search_loc':
          edifice_id = request.POST.get('edifice_id')
          if edifice_id:
            office_locs = Office_Loc.objects.filter(edifice_id=edifice_id)
            data = [{'id': ol.id, 'name': f"Piso {ol.floor} - Ala {ol.wing}"} for ol in office_locs]
          else:
            data = []

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

        if action == 'search_dependency':
          location_id = request.POST.get('location_id')

          dependencies = Dependency.objects.all()
          if location_id:
            dependencies = dependencies.filter(location_id=location_id)

          data = [{'id': d.id, 'name': d.dependency} for d in dependencies]

        elif action == 'search_edifice':
          location_id = request.POST.get('location_id')
          if location_id:
            edifices = Edifice.objects.filter(location_id=location_id)
            data = [{'id':e.id, 'name': e.edifice} for e in edifices]
          else:
            data = []

        elif action == 'search_loc':
          edifice_id = request.POST.get('edifice_id')
          if edifice_id:
            office_locs = Office_Loc.objects.filter(edifice_id=edifice_id)
            data = [{'id': ol.id, 'name': f"Piso {ol.floor} - Ala {ol.wing}"} for ol in office_locs]
          else:
            data = []

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

    if action =='search_dependency':
      location_id = post_data.get('location_id')
      dependencies = Dependency.objects.all()
      if location_id:
        try:
          location_id = int(location_id)
          dependencies = dependencies.filter(location_id=location_id)
          data = [{'id': d.id, 'name': d.dependency} for d in dependencies]
        except ValueError:
          pass

    elif action == 'search_edifice':
      location_id = post_data.get('location_id')
      if location_id:
        try:
          location_id = int(location_id)
          edifices = Edifice.objects.filter(location_id=location_id)
          data = [{'id':e.id, 'name': e.edifice} for e in edifices]
        except ValueError:
          pass

    elif action == 'search_loc':
      edifice_id = post_data.get('edifice_id')
      if edifice_id:
        try:
          edifice_id = int(edifice_id)
          office_locs = Office_Loc.objects.filter(edifice_id=edifice_id)
          data = [{'id': ol.id, 'name': f"Piso {ol.floor} - Ala {ol.wing}"} for ol in office_locs]
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

      office = self.get_object()

      form = context['form']

      if office.dependency:
        form.fields['dependency'].queryset = Dependency.objects.filter(location=office.dependency.location)
        form.initial['dependency'] = office.dependency.id

      if office.loc:
        form.fields['edifice'].queryset = Edifice.objects.filter(location=office.loc.edifice.location)
        form.fields['loc'].queryset = Office_Loc.objects.filter(edifice=office.loc.edifice)
        form.initial['edifice'] = office.loc.edifice.id
        form.initial['loc'] = office.loc.id

      form.fields['dependency'].widget.attrs.update({
        'data-preselected': office.dependency.id if office.dependency else ''
      })

      form.fields['edifice'].widget.attrs.update({
        'data-preselected': office.loc.edifice.id if office.loc.edifice else ''
      })

      form.fields['loc'].widget.attrs.update({
        'data-preselected': office.loc.id if office.loc else ''
      })
        # context['form'].fields['dependency'].queryset = Dependency.objects.filter(
        # location = office.dependency.location
      # )
# 
      # context['form'].fields['edifice'].queryset = Edifice.objects.filter(
        # location = office.loc.edifice.location,
      # )
# 
      # context['form'].fields['loc'].queryset = Office_Loc.objects.filter(
        # edifice=office.loc.edifice
      # )
# 
      # context['form'].initial['location'] = office.dependency.location.id if office.dependency.location else None
      # context['form'].initial['dependency'] = office.dependency.id if office.dependency else None
      # context['form'].initial['edifice'] = office.loc.edifice.id if office.loc.edifice.location else None
      # context['form'].initial['loc'] = office.loc.id if office.loc.edifice else None
# 
      # context['form'].fields['dependency'].widget.attrs.update({
        # 'data-preselected': self.object.dependency.id if self.object.dependency else ''
      # })
      # context['form'].fields['edifice'].widget.attrs.update({
        # 'data-preselected': self.object.loc.edifice.id if self.object.loc.edifice else ''
      # })
      # context['form'].fields['loc'].widget.attrs.update({
        # 'data-preselected': self.object.loc.id if self.object.loc else ''
      # })
# 
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