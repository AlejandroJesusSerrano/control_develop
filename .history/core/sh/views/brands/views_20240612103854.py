from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import BrandForm
from core.sh.models import Brand


class BrandListView(ListView):
  model = Brand
  template_name = 'brand/list.html'

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

  def post(self, request, *args, **kwargs):
    data={}
    try:
      action = request.POST.get('action')
      if action == 'add':
        form = self.get_form()
        data = form.save()
      else:
        data['error'] = 'Acción no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Marcas de Dispositivos'
    context['title'] = 'Agregar una Marca'
    context['btn_add_id'] = 'brand_add'
    context['entity'] = 'Marcas'
    context['list_url'] = reverse_lazy('sh:brand_list')
    context['form_id'] = 'brandForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class BrandUpadateView(UpdateView):
  model = Brand
  form_class = BrandForm
  template_name = 'brand/create.html'
  success_url = reverse_lazy('sh:brand_list')

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
        data = form.save()
      else:
        data['error'] = 'Accion no válida'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Marcas de Dispositivos'
      context['title'] = 'Editar el Nombre de una Marca'
      context['btn_add_id'] = 'brand_add'
      context['entity'] = 'Marcas'
      context['list_url'] = reverse_lazy('sh:brand_list')
      context['form_id'] = 'brandForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
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
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context