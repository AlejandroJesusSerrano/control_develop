from urllib import request
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms.edifice.forms import EdificeForm
from core.sh.models import Edifice, Location, Province

# Ajax View
@csrf_protect
def ajax_edifice_search_location(request):
  data = []
  if request.method == 'POST':
    province_id = request.POST.get('province_id')
    locations = Location.objects.filter(province_id=province_id)
    data = [{'id': l.id, 'name': l.location} for l in locations]
  return JsonResponse(data, safe=False)

class EdificeListView(ListView):
  model = Edifice
  template_name = 'edifice/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        edifices = Edifice.objects.all()
        data = [e.toJSON() for e in edifices]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

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
  model = Edifice
  form_class = EdificeForm
  template_name = 'edifice/create.html'
  success_url = reverse_lazy('sh:edifice_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data= {
          'success': True,
          'message': 'Edificio agregado correctamente',
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-reuquested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status=400)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({"error": errors}, status=400)
    else:
      return super().form_invlid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Edificios'
    context['title'] = 'Agregar un Edificio'
    context['btn_add_id'] = 'edifice_add'
    context['entity'] = 'Edificios'
    context['list_url'] = reverse_lazy('sh:edifice_list')
    context['form_id'] = 'edificeForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-custom-primary'
    context['filter_btn_color'] = 'btn-primary'
    return context

class EdificeUpdateView(UpdateView):
  model = Edifice
  form_class = EdificeForm
  template_name = 'edifice/create.html'
  success_url = reverse_lazy('sh:edifice_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Edificio actualizado exitosamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)

    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status=500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)
  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error': errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Edificios'
    context['title'] = 'Editar Edificio'
    context['btn_add_id'] = 'edifice_add'
    context['entity'] = 'Edificios'
    context['list_url'] = reverse_lazy('sh:edifice_list')
    context['form_id'] = 'edificeForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-custom-warning'
    context['filter_btn_color'] = 'bg-custom-warning'

    edifice = self.get_object()

    if edifice.location and edifice.location.province:
      context['form'].initial['province'] = edifice.location.province.id
      context['form'].initial['location'] = edifice.location.id if edifice.location else None
      context['form'].fields['province'].widget.attrs.update({
      'data-preselected': self.object.location.province.id if self.object.location and self.object.location.province else ''
      })
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
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context