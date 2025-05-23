from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator

from django.forms import HiddenInput
from core.sh.forms import Dev_ModelForm
from core.sh.models import Dev_Model
from core.sh.models.dev_type.models import Dev_Type


class Dev_ModelsListView(ListView): 
    model = Dev_Model
    template_name = 'dev_model/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Dev_Model.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Modelos de Dispositivos'
        context['title'] = 'Listado de Modelos'
        context['btn_add_id'] = 'dev_model_add'
        context['create_url'] = reverse_lazy('sh:dev_model_add')
        context['list_url'] = reverse_lazy('sh:dev_model_list')
        context['entity'] = 'Modelos de Dispositivos'
        context['nav_icon'] = 'fa-solid fa-laptop-file'
        context['table_id'] = 'dev_model_table'
        context['add_btn_title'] = 'Agregar Modelo de Dispositivo'
        return context

class Dev_ModelsCreateView(CreateView):
    model: Dev_Model
    form_class = Dev_ModelForm
    template_name = 'dev_model/create.html'
    success_url = reverse_lazy('sh:dev_model_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return ['dev_model/popup_add.html']
        return ['dev_model/create.html']

    def get_initial(self):
        initial = super().get_initial()
        context = self.request.GET.get('context')
        if context == 'switch':
            initial['dev_type'] = Dev_Type.objects.get(dev_type='SWITCH')
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        context = self.request.GET.get('context')
        if context == 'switch':
            form.fields['dev_type'].widget = HiddenInput()
            form.fields['dev_type'].initial = "SWITCH"
        if context == 'device':
            form.fields['dev_type'].queryset = Dev_Type.objects.exclude(dev_type='SWITCH')
        return form

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Tipo de Dispositivo agregado correctamente',
                    'dev_model_id': self.object.id,
                    'dev_model_name': self.object.dev_model,
                    'dev_model_brand': self.object.brand.brand
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
        context['page_title'] = 'Modelos de Dispositivos'
        context['title'] = 'Agregar un Modelo de Dispositivo'
        context['btn_add_id'] = 'dev_model_add'
        context['entity'] = 'Modelos de Dispositivos'
        context['list_url'] = reverse_lazy('sh:dev_model_list')
        context['form_id'] = 'dev_modelForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['btn_color'] = 'bg-custom-primary'
        return context

class Dev_ModelsUpadateView(UpdateView):
    model = Dev_Model
    form_class = Dev_ModelForm
    template_name = 'dev_model/create.html'
    success_url = reverse_lazy('sh:dev_model_list')

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
        context['page_title'] = 'Modelos de Dispositivos'
        context['title'] = 'Editar un Modelo de Dispositivo'
        context['btn_add_id'] = 'dev_model_add'
        context['entity'] = 'Modelos de Dispositivos'
        context['list_url'] = reverse_lazy('sh:dev_model_list')
        context['form_id'] = 'dev_modelForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['btn_color'] = 'bg-custom-warning'
        return context

class Dev_ModelsDeleteView(DeleteView):
    model = Dev_Model
    template_name = 'dev_model/delete.html'
    success_url = reverse_lazy('sh:dev_model_list')

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
        context['page_title'] = 'Modelos de Dispositivos'
        context['title'] = 'Eliminar un Modelo de Dispositivo'
        context['del_title'] = 'Model de Dispositivo: '
        context['list_url'] = reverse_lazy('sh:dev_model_list')
        context['form_id'] = 'dev_modelForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context

class Dev_ModelsDetailsView(DetailView):
    model = Dev_Model
    template_name = 'dev_model/modal_details.html'
    context_object_name = 'model'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render (request, self.template_name, context)
        else:
            return super().get(request, *args, **kwargs)