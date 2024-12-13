from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict

from core.sh.forms import WallPortForm
from core.sh.models import Wall_Port
from core.sh.models.location.models import Location
from core.sh.models.province.models import Province


class WallPortListView(ListView):
  model = Wall_Port
  template_name = 'wall_port/list.html'

  @method_decorator(login_required)

  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Wall_Port.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      return JsonResponse({'error':str(e)}, status = 400)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Puertos de la Pared'
    context['title'] = 'Listado de Puertos de la Pared'
    context['btn_add_id'] = 'wall_port_add'
    context['create_url'] = reverse_lazy('sh:wall_port_add')
    context['list_url'] = reverse_lazy('sh:wall_port_list')
    context['entity'] = 'Puertos de la Pared'
    context['nav_icon'] = 'fa-solid fa-ethernet'
    context['table_id'] = 'wall_port_table'
    return context

class WallPortCreateView(CreateView):
  model: Wall_Port
  form_class = WallPortForm
  template_name = 'wall_port/create.html'
  success_url = reverse_lazy('sh:wall_port_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Puerto de Pared agregado exitosamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status=500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error': errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Puertos de la Pared'
    context['title'] = 'Agregar una Puerto de la Pared'
    context['btn_add_id'] = 'wall_port_add'
    context['entity'] = 'Puertos de la Pared'
    context['list_url'] = reverse_lazy('sh:wall_port_list')
    context['form_id'] = 'wall_portForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    context['filter_body_color'] = 'bg-secondary'
    return context

class WallPortUpdateView(UpdateView):
  model = Wall_Port
  form_class = WallPortForm
  template_name = 'wall_port/create.html'
  success_url = reverse_lazy('sh:wall_port_list')

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
        if form.is_valid():
          instance = form.save()
          data = model_to_dict(instance)
        else:
          data ['error'] = form.errors
      else:
        data['error'] = 'Accion no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      wall_port = self.get_object()

      if wall_port.office and wall_port.office.loc and wall_port.office.loc.edifice and wall_port.office.loc.edifice.location and wall_port.office.loc.edifice.location.province and wall_port.office.dependency and ((wall_port.switch_port_in and wall_port.switch_port_in.switch and wall_port.switch_port_in.switch.rack) or (wall_port.switch_port_in and wall_port.switch_port_in.switch) or (wall_port.patch_port_in and wall_port.patch_port_in.patchera)):

        province = wall_port.office.loc.edifice.location.province
        context['form'].fields['province'].queryset = Province.objects.all()
        context['form'].initial['province'] = province.id

        location = wall_port.office.loc.edifice.location
        context['form'].fields['location'].queryset = Location.objects.filter(province=province)
        context['form'].initial['location'] = location.id


      context['page_title'] = 'Puertos de la Pared'
      context['title'] = 'Editar el Nombre de una Puerto de la Pared'
      context['btn_add_id'] = 'wall_port_add'
      context['entity'] = 'Puertos de la Pared'
      context['list_url'] = reverse_lazy('sh:wall_port_list')
      context['form_id'] = 'wall_portForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class WallPortDeleteView(DeleteView):
  model = Wall_Port
  template_name = 'wall_port/delete.html'
  success_url = reverse_lazy('sh:wall_port_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data={}
    try:
      self.object.delete()
    except Exception as e:
      JsonResponse = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Puertos de la Pared'
        context['title'] = 'Eliminar una Puerto de la Pared'
        context['del_title'] = 'Puerto de la Pared: '
        context['list_url'] = reverse_lazy('sh:wall_port_list')
        context['form_id'] = 'wall_portForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context