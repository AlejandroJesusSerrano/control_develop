from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms import SuplyForm
from core.sh.models import Suply
from core.sh.models.brands.models import Brand
from core.sh.models.dev_model.models import Dev_Model


class SuplyListView(ListView):
  model = Suply
  template_name = 'suply/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        suplyes = Suply.objects.all()
        data = [s.toJSON() for s in suplyes]
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data = {'error': str(e)}

    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Insumos'
    context['title'] = 'Listado de Insumos'
    context['btn_add_id'] = 'suply_add'
    context['create_url'] = reverse_lazy('sh:suply_add')
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['entity'] = 'Insumos'
    context['nav_icon'] = 'fa fa-boxes-stacked'
    context['table_id'] = 'suply_table'
    return context

class SuplyCreateView(CreateView):
  model: Suply
  form_class = SuplyForm
  template_name = 'suply/create.html'
  success_url = reverse_lazy('sh:suply_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'suply agregado exitosamente',
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
    context['page_title'] = 'Insumos'
    context['title'] = 'Agregar un Insumo'
    context['btn_add_id'] = 'suply_add'
    context['entity'] = 'Insumos'
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['form_id'] = 'suplyForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-custom-primary'
    return context

class SuplyUpadateView(UpdateView):
  model = Suply
  form_class = SuplyForm
  template_name = 'suply/create.html'
  success_url = reverse_lazy('sh:suply_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'suply actualizado exitosamente',
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
    context['page_title'] = 'Insumos'
    context['title'] = 'Editar Insumo'
    context['btn_add_id'] = 'suply_add'
    context['entity'] = 'Insumos'
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['form_id'] = 'suplyForm'
    context['action'] = 'edit'
    context['bg_color'] = 'bg-custom-warning'

    suply = self.get_object()

    if suply.dev_model:
      context['form'].fields['brand'].queryset = Brand.objects.filter(
        models_brand__dev_type=suply.dev_model.dev_type
      ).distinct()

      context['form'].fields['dev_model'].queryset = Dev_Model.objects.filter(
        dev_type=suply.dev_model.dev_type,
        brand=suply.dev_model.brand
    )

    context['form'].initial['brand'] = suply.dev_model.brand.id if suply.dev_model and suply.dev_model.brand else None
    context['form'].initial['dev_type'] = suply.dev_model.dev_type.id if suply.dev_model and suply.dev_model.dev_type else 'suply'
    context['form'].initial['dev_model'] = suply.dev_model.id if suply.dev_model else None

    context['form'].fields['brand'].widget.attrs.update({
      'data-preselected': self.object.dev_model.brand.id if self.object.dev_model and self.object.dev_model.brand else ''
    })
    context['form'].fields['dev_model'].widget.attrs.update({
      'data-preselected': self.object.dev_model.id if self.object.dev_model else ''
    })

    return context

class SuplyDeleteView(DeleteView):
  model = Suply
  template_name = 'suply/delete.html'
  success_url = reverse_lazy('sh:suply_list')

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
    context['page_title'] = 'Insumos'
    context['title'] = 'Eliminar un Insumo'
    context['del_title'] = 'Insumo: '
    context['list_url'] = reverse_lazy('sh:suply_list')
    context['form_id'] = 'suplyForm'
    context['bg_color'] = 'bg-custom-danger'
    context['action'] = 'delete'
    return context