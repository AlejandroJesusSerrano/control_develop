from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms import SwitchPortForm
from core.sh.models import Switch_Port

class Switch_PortListView(ListView):
    model = Switch_Port
    template_name = 'switch_port/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'searchdata':
                data = [i.toJSON() for i in Switch_Port.objects.all()]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Puertos de Switches'
        context['title'] = 'Listado de Puertos de Switches'
        context['btn_add_id'] = 'switch_port_add'
        context['create_url'] = reverse_lazy('sh:switch_port_add')
        context['list_url'] = reverse_lazy('sh:switch_port_list')
        context['entity'] = 'Puertos de Switches'
        context['nav_icon'] = 'fa-solid fa-ethernet'
        context['table_id'] = 'switch_port_table'
        return context

class Switch_PortCreateView(CreateView):
    model = Switch_Port
    form_class = SwitchPortForm
    template_name = 'switch_port/create.html'
    success_url = reverse_lazy('sh:switch_port_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Puerto de Switch agregado correctamente'
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
        context['page_title'] = 'Puertos de Switches'
        context['title'] = 'Agregar un Puerto de Switch'
        context['btn_add_id'] = 'switch_port_add'
        context['entity'] = 'Puertos de Switches'
        context['list_url'] = reverse_lazy('sh:switch_port_list')
        context['form_id'] = 'switch_portForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-primary'
        return context

class Switch_PortUpdateView(UpdateView):
    model = Switch_Port
    form_class = SwitchPortForm
    template_name = 'switch_port/create.html'
    success_url = reverse_lazy('sh:switch_port_list')

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
        context['page_title'] = 'Puertos de Switches'
        context['title'] = 'Editar un Puerto de Switch'
        context['btn_add_id'] = 'switch_port_add'
        context['entity'] = 'Puertos de Switches'
        context['list_url'] = reverse_lazy('sh:switch_port_list')
        context['form_id'] = 'switch_portForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-warning'
        return context

class Switch_PortDeleteView(DeleteView):
    model = Switch_Port
    template_name = 'switch_port/delete.html'
    success_url = reverse_lazy('sh:switch_port_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['success'] = True
            data['message'] = 'Puerto de Switch eliminado correctamente'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Puertos de Switches'
        context['title'] = 'Eliminar un Puerto de Switch'
        context['del_title'] = 'Puerto de Switch: '
        context['list_url'] = reverse_lazy('sh:switch_port_list')
        context['form_id'] = 'switch_portForm'
        context['bg_color'] = 'bg-danger'
        context['action'] = 'delete'
        return context
