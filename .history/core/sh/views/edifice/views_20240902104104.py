from urllib import request
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import EdificeForm
from core.sh.models import Edifice, Location


class EdificeListView(ListView):
  model = Edifice
  template_name = 'edifice/list.html'

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
        for i in Edifice.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Edificios'
    context['title'] = 'Listado de edificios'
    context['btn_add_id'] = 'edifice_add'
    context['create_url'] = reverse_lazy('sh:edifice_add')
    context['list_url'] = reverse_lazy('sh:edifice_list') 
    context['entity'] = 'Edificios'
    context['nav_icon'] = 'fa fa-building'
    context['table_id'] = 'edifice_table'
    return context

class EdificeCreateView(CreateView):
  model: Edifice
  form_class = EdificeForm
  template_name = 'edifice/create.html'
  success_url = reverse_lazy('sh:edifice_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')
        print(f"Accion recibida: {action}")

        if action == 'search_locations':
          province_id = request.POST.get('province_id')
          locations = Location.objects.filter(province_id=province_id)
          data = [{'id': l.id, 'name': l.location} for l in locations]

        else:
          form = EdificeForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Edificio guardado correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar el edificio: {str(e)}"}, status=400)
          else:
            errors = form.errors.get_json_data()
            print(f"Errores del formulario: {errors}")
            return JsonResponse({"error": "Formulario no valido", "form_errors":errors}, status=400)

        return JsonResponse(data, safe=False)

      except Exception as e:
        return JsonResponse({'error': str(e)}, status=400, safe=False)

    else:
      return super().post(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Edificios'
    context['title'] = 'Agregar un Edificio'
    context['btn_add_id'] = 'edifice_add'
    context['entity'] = 'Edificios'
    context['list_url'] = reverse_lazy('sh:edifice_list')
    context['form_id'] = 'edificeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class EdificeUpadateView(UpdateView):
  model = Edifice
  form_class = EdificeForm
  template_name = 'edifice/create.html'
  success_url = reverse_lazy('sh:edifice_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      data = {}
      try:
        action = request.POST.get('action')
        print(f"Accion recibida: {action}")

        if action == 'search_locations':
          province_id = request.POST.get('province_id')
          locations = Location.objects.filter(province_id=province_id)
          data = [{'id': l.id, 'name': l.location} for l in locations]

        else:
          form = EdificeForm(request.POST)
          if form.is_valid():
            try:
              form.save()
              return JsonResponse({"success": "Edificio guardado correctamente"}, status=200)
            except Exception as e:
              return JsonResponse({"error":f"Error al guardar el edificio: {str(e)}"}, status=400)
          else:
            errors = form.errors.get_json_data()
            print(f"Errores del formulario: {errors}")
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

      if action =='search_locations':
        province_id = request.POST.get('province_id')
        if province_id:
          locations = Location.objects.filter(province_id=province_id)
          data = [{'id': l.id, 'name': l.location} for l in locations]
        else:
          data = {'Error': 'No se proporcionó un ID de provincia válido'}

      return data

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Edificios'
    context['title'] = 'Editar Edificio'
    context['btn_add_id'] = 'edifice_add'
    context['entity'] = 'Edificios'
    context['list_url'] = reverse_lazy('sh:edifice_list')
    context['form_id'] = 'edificeForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-warning'

    edifice = self.get_object()

    context['form'].fields['location'].queryset = Location.objects.filter(
      province = edifice.location.province
    )

    context['form'].initial['province'] = edifice.location.province.id if edifice.location.province else None

    context['form'].fields['location'].widget.attrs.update({
      'data-preselected': self.object.location.id if self.object.location else ''
    })

    return context

class EdificeDeleteView(DeleteView):
  model = Edifice
  template_name = 'edifice/delete.html'
  success_url = reverse_lazy('sh:edifice_list')

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
        context['page_title'] = 'Edificios'
        context['title'] = 'Eliminar un Edificio'
        context['del_title'] = 'Edificio: '
        context['list_url'] = reverse_lazy('sh:edifice_list')
        context['form_id'] = 'edificeForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context