from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from core.sh.forms import ProvinceForm
from core.sh.models import Province


class ProvinceListView(ListView):
  model = Province
  template_name='province/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
     return super().dispatch(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Province.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Provincias'
    context['title'] = 'Listado de Provincias'
    context['btn_add_id'] = 'province_add'
    context['create_url'] = reverse_lazy('sh:province_add')
    context['list_url'] = reverse_lazy('sh:province_list')
    context['entity'] = 'Provincias'
    context['nav_icon'] = 'fa-solid fa-earth-americas'
    context['table_id'] = 'province_table'
    return context

class ProvinceCreateView(CreateView):
  model = Province
  form_class = ProvinceForm
  template_name = 'province/create.html'
  success_url = reverse_lazy('sh:province_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
     return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Provincia agregada correctamente',
          'province_id': self.object.id,
          'province_name': self.object.province,
          'number_id': self.object.number_id
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
      context['page_title'] = 'Provincias'
      context['title'] = 'Agregar una Provincia'
      context['btn_add_id'] = 'prov_add'
      context['entity'] = 'Provincias'
      context['list_url'] = reverse_lazy('sh:province_list')
      context['form_id'] = 'provForm'
      context['action'] = 'add'
      context['bg_color'] = 'bg-custom-primary'
      context['saved'] = kwargs.get('saved', None)
      return context

class ProvinceUpdateView(UpdateView):
  model = Province
  form_class = ProvinceForm
  template_name = 'province/create.html'
  success_url = reverse_lazy('sh:province_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Provincia actualizada exitosamente',
          'province_id': self.object.id,
          'province_name': self.object.province,
          'number_id': self.object.number_id
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
      return JsonResponse({"error": errors}, status=400)
    else:
      return super().form_invalid(form)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Provincias'
      context['title'] = 'Editar Datos de una Provincia'
      context['btn_add_id'] = 'prov_add'
      context['entity'] = 'Provincias'
      context['list_url'] = reverse_lazy('sh:province_list')
      context['form_id'] = 'provForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-custom-warning'
      context['saved'] = kwargs.get('saved', None)
      return context

class ProvinceDeleteView(DeleteView):
    model = Province
    template_name = 'province/delete.html'
    success_url = reverse_lazy('sh:province_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Provincias'
        context['title'] = 'Eliminar una Provincia'
        context['del_title'] = 'Provincia: '
        context['list_url'] = reverse_lazy('sh:province_list')
        context['form_id'] = 'provForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context