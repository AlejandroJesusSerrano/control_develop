from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from core.sh.forms import PatchPortForm
from core.sh.models import Patch_Port


class Patch_PortListView(ListView):
    model = Patch_Port
    template_name = 'patch_port/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'searchdata':
                data = [i.toJSON() for i in Patch_Port.objects.all()]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Puertos Patcheras'
        context['title'] = 'Listado de Puertos Patcheras'
        context['btn_add_id'] = 'patch_port_add'
        context['create_url'] = reverse_lazy('sh:patch_port_add')
        context['list_url'] = reverse_lazy('sh:patch_port_list')
        context['entity'] = 'Puertos Patcheras'
        context['nav_icon'] = 'fa fa-copyright'
        context['table_id'] = 'patch_port_table'
        context['add_btn_title'] = 'Agregar Puerto de Patchera'
        return context

class Patch_PortCreateView(CreateView):
    model: Patch_Port
    form_class = PatchPortForm
    template_name = 'patch_port/create.html'
    success_url = reverse_lazy('sh:patch_port_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return ['patch_port/popup_add.html']
        return ['patch_port/create.html']

    def form_valid(self, form):
        try:

            self.object = form.save()
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Puerto de Patchera agregado correctamente',
                    'patch_port_id': self.object.id,
                    'patch_port_name': self.object.port,
                    'patch_port_patchera': self.object.patchera.patchera,
                    'patch_port_rack': self.object.patchera.rack.rack,
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
        context['page_title'] = 'Puertos Patcheras'
        context['title'] = 'Agregar un Puerto de Patchera'
        context['btn_add_id'] = 'patch_port_add'
        context['entity'] = 'Puertos Patcheras'
        context['list_url'] = reverse_lazy('sh:patch_port_list')
        context['form_id'] = 'patch_portForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['btn_color'] = 'bg-custom-primary'
        return context

class Patch_PortUpadateView(UpdateView):
    model = Patch_Port
    form_class = PatchPortForm
    template_name = 'patch_port/create.html'
    success_url = reverse_lazy('sh:patch_port_list')

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
                    'message': 'Puerto de Switch actualizado correctamente'
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
        context['page_title'] = 'Puertos Patcheras'
        context['title'] = 'Editar el Puerto de una Patchera'
        context['btn_add_id'] = 'patch_port_add'
        context['entity'] = 'Puertos Patcheras'
        context['list_url'] = reverse_lazy('sh:patch_port_list')
        context['form_id'] = 'patch_portForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['btn_color'] = 'bg-custom-warning'
        return context

class Patch_PortDeleteView(DeleteView):
    model = Patch_Port
    template_name = 'patch_port/delete.html'
    success_url = reverse_lazy('sh:patch_port_list')

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
        context['page_title'] = 'Puertos Patcheras'
        context['title'] = 'Eliminar un Puerto de Patchera'
        context['del_title'] = 'Puerto Patchera: '
        context['list_url'] = reverse_lazy('sh:patch_port_list')
        context['form_id'] = 'patch_portForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        context['btn_color'] = 'bg-custom-danger'
        return context

@csrf_protect
@require_http_methods(['GET'])
def get_patch_ports_by_rack(request):
    patchera_id = request.GET.get('patchera_id')
    if patchera_id:
        try:
            patch_ports = Patch_Port.objects.filter(patchera_id=patchera_id).values('id', 'port', 'pathcera', 'patchera__rack', 'patchera__rack__office')
            return JsonResponse(list(patch_ports), safe=False)
        except Exception as e:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)

@csrf_protect
@require_http_methods(['GET'])
def get_patch_ports_by_office(request):
    office_id = request.GET.get('office_id')
    if office_id:
        try:
            patch_ports = Patch_Port.objects.filter(office_id=office_id).values('id', 'port', 'pathcera', 'patchera__rack', 'patchera__rack__office')
            return JsonResponse(list(patch_ports), safe=False)
        except Exception as e:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)