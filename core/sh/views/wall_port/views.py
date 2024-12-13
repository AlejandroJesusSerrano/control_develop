from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.db.models import Q

from core.sh.forms import WallPortForm
from core.sh.models import Wall_Port
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.province.models import Province
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.switch_port.models import Switch_Port


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
    context['filter_btn_color'] = 'btn-primary'

    return context

class WallPortUpdateView(UpdateView):
  model = Wall_Port
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
      context['title'] = 'Editar el Nombre de una Puerto de la Pared'
      context['btn_add_id'] = 'wall_port_add'
      context['entity'] = 'Puertos de la Pared'
      context['list_url'] = reverse_lazy('sh:wall_port_list')
      context['form_id'] = 'wall_portForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      context['filter_btn_color'] = 'btn-warning'

      wall_port = self.get_object()

      if (
        wall_port.office and
        wall_port.office.loc and
        wall_port.office.loc.edifice and
        wall_port.office.loc.edifice.location and
        wall_port.office.loc.edifice.location.province and
        wall_port.office.dependency and
        wall_port.office.dependency.location
        ):

        province = wall_port.office.loc.edifice.location.province
        context['form'].fields['province'].queryset = Province.objects.all()
        context['form'].initial['province'] = province.id

        location = wall_port.office.loc.edifice.location
        context['form'].fields['location'].queryset = Location.objects.filter(province=province)
        context['form'].initial['location'] = location.id

        dependency = wall_port.office.dependency
        context['form'].fields['dependency'].queryset = Dependency.objects.filter(location=location)
        context['form'].initial['dependency'] = dependency.id

        edifice = wall_port.office.loc.edifice
        context['form'].fields['edifice'].queryset = Edifice.objects.filter(location=location)
        context['form'].initial['edifice'] = edifice.id

        loc = wall_port.office.loc
        context['form'].fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
        context['form'].initial['loc'] = loc.id

        office = wall_port.office
        context['form'].fields['office'].queryset = Office.objects.filter(loc=loc)
        context['form'].initial['office'] = office.id

        rack = None
        if wall_port.switch_port_in and wall_port.switch_port_in.switch:
          rack = wall_port.switch_port_in.switch.rack
        elif wall_port.patch_port_in and wall_port.patch_port_in.patchera:
          rack = wall_port.patch_port_in.patchera.rack

        if rack:
          context['form'].fields['rack'].queryset = Rack.objects.filter(Q(office=office))
          context['form'].initial['rack'] = rack.id

        switch = getattr(wall_port.switch_port_in, 'switch', None)
        if switch:
          context['form'].fields['switch'].queryset = Switch.objects.filter(Q(rack=rack) | Q(office=office))
          context['form'].initial['switch'] = switch.id

        patchera = getattr(wall_port.patch_port_in, 'patchera', None)
        if patchera:
          context['form'].fields['patchera'].queryset == Patchera.objects.filter(rack=rack)
          context['form'].initial['patchera'] = patchera.id

        switch_port_in = getattr(wall_port, 'switch_port_in', None)
        if switch_port_in:
          context['form'].fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch=switch)
          context['form'].initial['switch_port_in'] = switch_port_in.id

        patch_port_in = getattr(wall_port, 'patch_port_in', None)
        if patch_port_in:
          context['form'].fields['patch_port_in'].queryset = Patch_Port.objects.filter(patchera=patchera)
          context['form'].initial['patch_port_in'] = patch_port_in.id

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