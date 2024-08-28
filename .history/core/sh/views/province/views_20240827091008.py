from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages

from core.sh.forms import ProvinceForm
from core.sh.models import Province


class ProvinceListView(ListView):
  model = Province
  template_name='province/list.html'

  @method_decorator(csrf_exempt)
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
    form.save()
    return super().form_valid(form)

  def form_invalid(self, form):
    return self.render_to_response(self.get_context_data(form=form))

  # def post(self, request, *args, **kwargs):
  #   data = {}
  #   try:
  #     action = request.POST.get('action')
  #     form = self.get_form()
  #     if action == 'add' and form.is_valid():
  #       form.save()
  #       data['success'] = 'Provincia agregada exitosamente'
  #     else:
  #       data['error'] = form.errors.as_json()
  #   except Exception as e:
  #     data['error'] = str(e)
  #   return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Provincias'
      context['title'] = 'Agregar una Provincia'
      context['btn_add_id'] = 'prov_add'
      context['entity'] = 'Provincias'
      context['list_url'] = reverse_lazy('sh:province_list')
      context['form_id'] = 'provForm'
      context['action'] = 'add'
      context['bg_color'] = 'bg-primary'
      return context

class ProvinceUpdateView(UpdateView):
  model = Province
  form_class = ProvinceForm
  template_name = 'province/create.html'
  success_url = reverse_lazy('sh:province_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)

  def form_invalid(self, form):
    return self.render_to_response(self.get_context_data(form=form))


  # def post(self, request, *args, **kwargs):
  #   data = {}
  #   try:
  #     action = request.POST.get('action')
  #     if action == 'edit' :
  #       form = self.get_form()
  #       if form.is_valid():
  #         form.save()
  #         data = {'success': 'Provincia editada exitosamente'}
  #       else:
  #         data['error'] = form.errors
  #     else: data ['error'] = {'action': ['Acción no Válida']}
  #   except Exception as e:
  #     data['error'] = {'exception': [str(e)]}
  #   return JsonResponse(data)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['page_title'] = 'Provincias'
      context['title'] = 'Editar Datos de una Provincia'
      context['btn_add_id'] = 'prov_add'
      context['entity'] = 'Provincias'
      context['list_url'] = reverse_lazy('sh:province_list')
      context['form_id'] = 'provForm'
      context['action'] = 'edit'
      context['bg_color'] = 'bg-warning'
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
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context

class ProvinceFormView(FormView):
  form_class = ProvinceForm
  template_name = 'province/create.html'
  success_url = reverse_lazy('sh:province_list')

  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    print(form.is_valid())
    print(form)
    return super().form_valid(form)

  def form_invalid(self, form):
    print(form.is_valid())
    print(form.errors)
    return super().form_invalid(form)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Form | Province'
    context['entity'] = 'Provincias'
    context['list_url'] = reverse_lazy('sh:province_list')
    context['action'] = 'add'
    context['bg_color'] = 'bg-primary'
    return context