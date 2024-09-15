from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import Office_Loc_Form
from core.sh.models import Edifice, Office_Loc

class Office_Loc_ListView(ListView):
  model = Office_Loc
  template_name = 'office_loc/list.html'

  @method_decorator(login_required)
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST.get('action')
      if action == 'searchdata':
        office_locs = Office_Loc.objects.all()
        data = [ol.toJSON() for ol in office_locs]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Locaciones de Oficinas'
    context['title'] = 'Locación de Oficina'
    context['btn_add_id'] = 'office_loc_add'
    context['create_url'] = reverse_lazy('sh:office_loc_add')
    context['list_url'] = reverse_lazy('sh:office_loc_list')
    context['entity'] = 'Locación de Oficina'
    context['nav_icon'] = 'fa-solid fa-building'
    context['table_id'] = 'office_loc_table'
    return context

class Office_Loc_CreateView(CreateView):
  model = Office_Loc
  form_class = Office_Loc_Form
  template_name = "office_loc/create.html"
  success_url = reverse_lazy('sh:office_loc_list')

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')

        if action == 'search_edifice':
          location_id = request.POST.get('location_id')
          edifices = Edifice.objects.filter(location_id=location_id)
          data = [{'id':e.id, 'name': e.edifice} for e in edifices]

        else:
          form = Office_Loc_Form(request.POST)

          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Locación de Oficina guardada correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar la locación de oficina: {str(e)}"}, status=400)

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
    context['page_title'] = 'Locaciones de Oficinas'
    context['title'] = 'Agregar una Locación de Oficina'
    context['btn_add_id'] = 'office_loc_add'
    context['entity'] = 'Locación de Oficina'
    context['list_url'] = reverse_lazy('sh:office_loc_list')
    context['form_id'] = 'office_locForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class Office_Loc_UpdateView(UpdateView):
    model = Office_Loc
    form_class = Office_Loc_Form
    template_name = 'office_loc/create.html'
    success_url = reverse_lazy('sh:office_loc_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
      return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
      if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {}
        try:
          action = request.POST.get('action')

          if action == 'search_edifice':
            location_id = request.POST.get('location_id')
            edifices = Edifice.objects.filter(location_id=location_id)
            data = [{'id':e.id, 'name': e.edifice} for e in edifices]

          else:
            self.object = self.get_object()
            form = self.get_form()  # Se ha añadido para obtener el formulario con la instancia actual
            if form.is_valid():
              try:
                form.save()
                return JsonResponse({"success": "Locación de Oficina actualizada correctamente"}, status=200)
              except Exception as e:
                return JsonResponse({"error": f"Error al actualizar la locación de oficina: {str(e)}"}, status=400)
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

      if action == 'search_edifice':
        location_id = post_data.get('location_id')
        if location_id:
          try:
            location_id = int(location_id)
            edifices = Edifice.objects.filter(location_id=location_id)
            data = [{'id':e.id, 'name': e.edifice} for e in edifices]
          except ValueError:
            pass

      return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Locaciones de Oficinas'
        context['title'] = 'Editar Locación de Oficina'
        context['btn_add_id'] = 'office_loc_add'
        context['entity'] = 'Locación de Oficina'
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['form_id'] = 'office_locForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-warning'

        office_loc = self.get_object()

        context['form'].fields['edifice'].queryset = Edifice.objects.filter(
          location = office_loc.edifice.location
        )

        context['form'].initial['location'] = office_loc.edifice.location.id if office_loc.edifice.location else None
        context['form'].initial['edifice'] = office_loc.edifice.id if office_loc.edifice else None

        context['form'].fields['edifice'].widget.attrs.update({
          'data-preselected': self.object.edifice.id if self.object.edifice else ''
        })

        return context

class Office_Loc_DeleteView(DeleteView):
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
        context['page_title'] = 'Locaciones de Oficinas'
        context['title'] = 'Eliminar una Locaión de Oficina'
        context['del_title'] = 'Locación de Oficina: '
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['form_id'] = 'office_locForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context