from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms.brands.forms import BrandForm
from core.sh.models import Brand


class BrandListView(ListView):
  model = Brand
  template_name = 'brand/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Brand.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Marcas de Dispositivos'
    context['title'] = 'Listado de Marcas de Dispositivos'
    context['btn_add_id'] = 'brand_add'
    context['create_url'] = reverse_lazy('sh:brand_add')
    context['list_url'] = reverse_lazy('sh:brand_list')
    context['entity'] = 'Marcas'
    context['nav_icon'] = 'fa fa-copyright'
    context['table_id'] = 'brand_table'
    return context

class BrandCreateView(CreateView):
  model: Brand
  form_class = BrandForm
  template_name = 'brand/create.html'
  success_url = reverse_lazy('sh:brand_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Marca agregada exitosamente',
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': str(e)}, status = 500)
      else:
        form.add_error(None, str(e))
        return self.form_invalid(form)

  def form_invalid(self, form):
    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
      errors = form.errors.get_json_data()
      return JsonResponse({'error': errors}, status=400)
    else:
      return super().form_invalid(form)

  def post(self, request, *args, **kwargs):
    return super().post(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Marcas de Dispositivos'
    context['title'] = 'Agregar una Marca'
    context['btn_add_id'] = 'brand_add'
    context['entity'] = 'Marcas'
    context['list_url'] = reverse_lazy('sh:brand_list')
    context['form_id'] = 'brandForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-custom-primary'
    context['saved'] = kwargs.get('saved', None)
    return context

class BrandUpadateView(UpdateView):
  model = Brand
  form_class = BrandForm
  template_name = 'brand/create.html'
  success_url = reverse_lazy('sh:brand_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Marca actualizada exitosamente'
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
      context['page_title'] = 'Marcas de Dispositivos'
      context['title'] = 'Editar el Nombre de una Marca'
      context['btn_add_id'] = 'brand_add'
      context['entity'] = 'Marcas'
      context['list_url'] = reverse_lazy('sh:brand_list')
      context['form_id'] = 'brandForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-custom-warning'
      context['saved'] = kwargs.get('saved', None)
      return context

class BrandDeleteView(DeleteView):
  model = Brand
  template_name = 'brand/delete.html'
  success_url = reverse_lazy('sh:brand_list')

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
        context['page_title'] = 'Marcas de Dispositivos'
        context['title'] = 'Eliminar una Marca'
        context['del_title'] = 'Marca: '
        context['list_url'] = reverse_lazy('sh:brand_list')
        context['form_id'] = 'brandForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context