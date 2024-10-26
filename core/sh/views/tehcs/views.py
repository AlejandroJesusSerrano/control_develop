from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.sh.forms import TechsForm
from core.sh.models import Techs


class TechsListView(ListView):
  model = Techs
  template_name = 'techs/list.html'

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def post (self, request, *args, **kwargs):
    data = {}
    try:
      action = request.POST['action']
      if action == 'searchdata':
        data = []
        for i in Techs.objects.all():
          data.append(i.toJSON())
      else:
        data['error'] = 'Ha ocurrido un error'
    except Exception as e:
      data['error'] = str(e)
    return JsonResponse(data, safe=False)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['page_title'] = 'Técnicos'
    context['title'] = 'Listado de Técnicos'
    context['btn_add_id'] = 'techs_add'
    context['create_url'] = reverse_lazy('sh:techs_add')
    context['list_url'] = reverse_lazy('sh:techs_list')
    context['entity'] = 'Técnicos'
    context['nav_icon'] = 'fa fa-helmet-safety'
    context['table_id'] = 'techs_table'
    return context

class TechsCreateView(CreateView):
  model: Techs
  form_class = TechsForm
  template_name = 'techs/create.html'
  success_url = reverse_lazy('sh:techs_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'success': True,
          'message': 'Tipo de Dispositivo agregado correctamente',
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
    context['page_title'] = 'Técnicos'
    context['title'] = 'Agregar un Técnico'
    context['btn_add_id'] = 'techs_add'
    context['entity'] = 'Técnicos'
    context['list_url'] = reverse_lazy('sh:techs_list')
    context['form_id'] = 'techsForm'
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context

class TechsUpadateView(UpdateView):
  model = Techs
  form_class = TechsForm
  template_name = 'techs/create.html'
  success_url = reverse_lazy('sh:techs_list')

  @method_decorator(login_required)
  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    try:
      self.object = form.save()

      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
          'succes': True,
          'message': 'Tipo de Dispositivo actualizado exitosamente'
        }
        return JsonResponse(data)
      else:
        return super().form_valid(form)
    except Exception as e:
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error':str(e)}, status=500)
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
      context['page_title'] = 'Técnicos'
      context['title'] = 'Editar Técnico'
      context['btn_add_id'] = 'Techs_add'
      context['entity'] = 'Técnicos'
      context['list_url'] = reverse_lazy('sh:techs_list')
      context['form_id'] = 'techsForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
      return context

class TechsDeleteView(DeleteView):
  model = Techs
  template_name = 'techs/delete.html'
  success_url = reverse_lazy('sh:techs_list')

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
        context['page_title'] = 'Técnicos'
        context['title'] = 'Eliminar un Técnico'
        context['del_title'] = 'Técnico: '
        context['list_url'] = reverse_lazy('sh:techs_list')
        context['form_id'] = 'techsForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context