from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator

from core.sh.forms.switch.forms import SwitchForm
from core.sh.models import Brand, Dependency, Dev_Model, Dev_Type, Edifice, Office, Switch, Location
from core.sh.models.device.models import Device
from core.sh.models.wall_port.models import Wall_Port

class SwitchListView(ListView):
    model = Switch
    template_name = 'switch/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                switches = Switch.objects.all()
                data = [s.toJSON() for s in switches]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Switchs'
        context['title'] = 'Listado de Switchs'
        context['btn_add_id'] = 'switch_add'
        context['create_url'] = reverse_lazy('sh:switch_add')
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['entity'] = 'Switchs'
        context['nav_icon'] = 'fa fa-copyright'
        context['table_id'] = 'switch_table'
        context['add_btn_title'] = 'Agregar Switch'
        return context

class SwitchCreateView(CreateView):
    model = Switch
    form_class = SwitchForm
    template_name = 'switch/create.html'
    success_url = reverse_lazy('sh:switch_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        switch_wall_ports = Switch.objects.filter(wall_port_in__isnull=False).values_list('wall_port_in', flat=True)
        device_wall_ports = Device.objects.filter(wall_port_in__isnull=False).values_list('wall_port_in', flat=True)
        used_wall_ports = set(switch_wall_ports) | set(device_wall_ports)

        form.fields['wall_port_in'].queryset = Wall_Port.objects.exclude(id__in=used_wall_ports)
        return form

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return['switch/popup_add.html']
        return ['switch/create.html']

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Switch agregado exitosamente',
                    'switch_id': self.object.id,
                    'switch_name': f'{self.object.model.brand.brand} {self.object.model.dev_model} DE {self.object.ports_q} PUERTOS',
                    'switch_model': self.object.model.dev_model,
                    'switch_brand': self.object.model.brand.brand,
                    'switch_ports_q': self.object.ports_q,
                    'switch_ip': self.object.ip,
                    'switch_rack': f'RACK: {self.object.rack.rack} EN OFICINA: {self.object.rack.office.office}' if self.object.rack else 'No se encuentra en Rack',
                    'switch_rack_pos': self.object.switch_rack_pos if self.object.rack else 'No se encuentra en Rack',
                    'switch_office': self.object.office.office if self.object.office else 'No se encuentra en oficina',
                    'switch_wall_port_in': str(self.object.wall_port_in) if self.object.wall_port_in else 'No ingresa de pared',
                    'switch_switch_port_in': str(self.object.switch_port_in) if self.object.switch_port_in else 'No ingresa de switch',
                    'switch_patch_port_in': str(self.object.patch_port_in) if self.object.patch_port_in else 'No ingresa de patchera',
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
        context['page_title'] = 'Switchs'
        context['title'] = 'Agregar una Switch'
        context['btn_add_id'] = 'switch_add'
        context['entity'] = 'Switchs'
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['form_id'] = 'switchForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['filter_btn_color'] = 'btn-primary'
        context['dev_type_id'] = 'SWITCH'
        context['btn_color'] = 'btn-primary'
        return context

class SwitchUpdateView(UpdateView):
    model = Switch
    form_class = SwitchForm
    template_name = 'switch/create.html'
    success_url = reverse_lazy('sh:switch_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        switch_wall_ports = Switch.objects.filter(wall_port_in__isnull=False).values_list('wall_port_in_id', flat=True)
        device_wall_ports = Device.objects.filter(wall_port_in__isnull=False).values_list('wall_port_in_id', flat=True)
        used_wall_ports = set(switch_wall_ports) | set(device_wall_ports)

        current_wall_port = self.get_object().wall_port_in
        if current_wall_port:
            form.fields['wall_port_in'].queryset = Wall_Port.objects.exclude(
                id__in=used_wall_ports
            ) | Wall_Port.objects.filter(id=current_wall_port.id)
        else:
            form.fields['wall_port_in'].queryset = Wall_Port.objects.exclude(id__in=used_wall_ports)
        return form

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Switch actualizado exitosamente',
                    'switch_id': self.object.id,
                    'switch_name': f'{self.object.model.brand.brand} {self.object.model.dev_model} DE {self.object.ports_q} PUERTOS',
                    'switch_model': self.object.model.dev_model,
                    'switch_brand': self.object.model.brand.brand,
                    'switch_ports_q': self.object.ports_q,
                    'switch_ip': self.object.ip,
                    'switch_rack': f'RACK: {self.object.rack.rack} EN OFICINA: {self.object.rack.office.office if self.object.rack.office else "Desconocida"}' if self.object.rack else 'No se encuentra en Rack',
                    'switch_rack_pos': self.object.switch_rack_pos if self.object.rack else 'No se encuentra en Rack',
                    'switch_office': self.object.office.office if self.object.office else 'No se encuentra en oficina',
                    'switch_wall_port_in': str(self.object.wall_port_in) if self.object.wall_port_in else 'No ingresa de pared',
                    'switch_switch_port_in': str(self.object.switch_port_in) if self.object.switch_port_in else 'No ingresa de switch',
                    'switch_patch_port_in': str(self.object.patch_port_in) if self.object.patch_port_in else 'No ingresa de patchera',
                }
                return JsonResponse(data)
            else:
                return super().form_valid(form)
        except Exception as e:
            print(f"Error al actualizar el switch: {e}")
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
        context['switch_id'] = self.object.id
        context['page_title'] = 'Switchs'
        context['title'] = 'Editar un Switch'
        context['btn_add_id'] = 'switch_add'
        context['entity'] = 'Switchs'
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['form_id'] = 'switchForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['filter_btn_color'] = 'bg-custom-warning'
        context['btn_color'] = 'bg-custom-warning'

        switch = self.get_object()

        if switch.model:
            context['form'].fields['brand'].queryset = Brand.objects.filter(
                models_brand__dev_type=switch.model.dev_type
            ).distinct()

        context['form'].fields['model'].queryset = Dev_Model.objects.filter(
            dev_type=switch.model.dev_type,
            brand=switch.model.brand
        )

        if switch.office and switch.office.loc and switch.office.loc.edifice:
            context['form'].fields['edifice'].queryset = Edifice.objects.filter(
            location=switch.office.loc.edifice.location
        )

        if switch.office and switch.office.loc and switch.office.loc.edifice:
            context['form'].fields['office'].queryset = Office.objects.select_related('loc__edifice').filter(loc__edifice=switch.office.loc.edifice)
        else:
            context['form'].fields['office'].queryset = Office.objects.none()

        context['form'].initial['brand'] = switch.model.brand.id if switch.model and switch.model.brand else None
        context['form'].initial['dev_type'] = switch.model.dev_type.id if switch.model and switch.model.dev_type else 'SWITCH'
        context['form'].initial['model'] = switch.model.id if switch.model else None

        if switch.office and switch.office.loc and switch.office.loc.edifice:
            context['form'].initial['location'] = switch.office.loc.edifice.location.id
            context['form'].initial['edifice'] = switch.office.loc.edifice.id
            context['form'].initial['office'] = switch.office.id if switch.office else None

        context['form'].fields['brand'].widget.attrs.update({
            'data-preselected': self.object.model.brand.id if self.object.model and self.object.model.brand else ''
        })
        context['form'].fields['model'].widget.attrs.update({
            'data-preselected': self.object.model.id if self.object.model else ''
        })
        context['form'].fields['edifice'].widget.attrs.update({
            'data-preselected': self.object.office.loc.edifice.id if self.object.office and self.object.office.loc and self.object.loc.edifice else ''
        })
        context['form'].fields['office'].widget.attrs.update({
            'data-preselected': self.object.office.id if self.object.office else ''
        })

        return context

class SwitchDeleteView(DeleteView):
    model = Switch
    template_name = 'switch/delete.html'
    success_url = reverse_lazy('sh:switch_list')

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

    def delete(self, request, *args, **kwargs):
        self.object.delete()
        try:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Switch eliminado exitosamente'})
            return super().delete(request, *args, **kwargs)
        except ValidationError as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            raise

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Switchs'
        context['title'] = 'Eliminar un Switch'
        context['del_title'] = 'Switch: '
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['form_id'] = 'switchForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context

class SwitchDetailsView(DetailView):
    model = Switch
    template_name = 'switch/modal_details.html'
    context_object_name = 'switch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        switch = self.object
        connections = []
        current = switch

        while current:
            next_connection = current.get_next_connection()
            if next_connection:
                connections.append(str(next_connection))
                current = next_connection
            else:
                current = None
        context['connections'] = connections
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, self.template_name, context)
        else:
            return super().get(request, *args, **kwargs)