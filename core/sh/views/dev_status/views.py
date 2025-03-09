from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms import Dev_StatusForm
from core.sh.models import Dev_Status


class DevStatusListView(ListView):
    model = Dev_Status
    template_name = 'dev_status/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Dev_Status.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Estados de los Dispositivos'
        context['title'] = 'Listado de Estados de los Dispositivos'
        context['btn_add_id'] = 'dev_status_add'
        context['create_url'] = reverse_lazy('sh:dev_status_add')
        context['list_url'] = reverse_lazy('sh:dev_status_list')
        context['entity'] = 'Estados de Dispositivos'
        context['nav_icon'] = 'fa fa-copyright'
        context['table_id'] = 'dev_status_table'
        context['add_btn_title'] = 'Agregar Nuevo Estado'
        return context

class Dev_StatusCreateView(CreateView):
    model: Dev_Status
    form_class = Dev_StatusForm
    template_name = 'dev_status/create.html'
    success_url = reverse_lazy('sh:dev_status_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return ['dev_status/popup_add.html']
        return ['dev_status/create.html']

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Estado de Dispositivo agregado correctamente.',
                    'dev_status_id': self.object.id,
                    'dev_status_name': self.object.dev_status
                }
                return JsonResponse(data)
            else:
                return super().form_invalid(form)
        except Exception as e:
            if self.request.heades.get('x-requested-with') == 'XMLHttpRequest':
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
        context['page_title'] = 'Estados de los Dispositivos'
        context['title'] = 'Agregar un Estado de Dispositivo'
        context['btn_add_id'] = 'dev_status_add'
        context['entity'] = 'Estados de Dispositivos'
        context['list_url'] = reverse_lazy('sh:dev_status_list')
        context['form_id'] = 'dev_statusForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        return context

class Dev_StatusUpadateView(UpdateView):
    model = Dev_Status
    form_class = Dev_StatusForm
    template_name = 'dev_status/create.html'
    success_url = reverse_lazy('sh:dev_status_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Estado de Dispositivo actualizado exitosamente'
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
        context['page_title'] = 'Estados de los Dispositivos'
        context['title'] = 'Editar el Nombre de un Estado de Dispositivo'
        context['btn_add_id'] = 'dev_status_add'
        context['entity'] = 'Estados de Dispositivos'
        context['list_url'] = reverse_lazy('sh:dev_status_list')
        context['form_id'] = 'dev_statusForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        return context

class Dev_StatusDeleteView(DeleteView):
    model = Dev_Status
    template_name = 'dev_status/delete.html'
    success_url = reverse_lazy('sh:dev_status_list')

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
        context['page_title'] = 'Estados de los Dispositivos'
        context['title'] = 'Eliminar un Estado de Dispositivo'
        context['del_title'] = 'Estado de Dispositivo: '
        context['list_url'] = reverse_lazy('sh:dev_status_list')
        context['form_id'] = 'dev_statusForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context