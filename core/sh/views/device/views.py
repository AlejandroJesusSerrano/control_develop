import traceback

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator

from core.sh.forms import DeviceForm
from core.sh.models import Device, Dev_Model, Employee, Office, Switch_Port, Wall_Port
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.location.models import Location
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.province.models import Province

class DeviceListView(ListView):
    model = Device
    template_name = 'device/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'searchdata':
                devices = Device.objects.all()
                data = [d.toJSON() for d in devices]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dispositivos'
        context['title'] = 'Listado de Dispositivos'
        context['btn_add_id'] = 'device_add'
        context['create_url'] = reverse_lazy('sh:device_add')
        context['list_url'] = reverse_lazy('sh:device_list')
        context['entity'] = 'Dispositivos'
        context['nav_icon'] = 'fa-solid fa-ethernet'
        context['table_id'] = 'device_table'
        context['add_btn_title'] = 'Agregar Dispositivo'
        return context

class DeviceCreateView(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = "device/create.html"
    success_url = reverse_lazy('sh:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return ['device/popup_add.html']
        return ['device/create.html']

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Switch agregado exitosamente',
                    'device_id': self.object.id,
                    'device_name': f"{self.object.dev_model.dev_type.dev_type} {self.object.dev_model.brand.brand} {self.object.dev_model.dev_model} S/N°: {self.object.serial_n}"
                }
                return JsonResponse(data)
            else:
                return super().form_valid(form)
        except Exception as e:
            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }, status=500)
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
        context['page_title'] = 'Dispositivos'
        context['title'] = 'Agregar un Dispositivo'
        context['btn_add_id'] = 'device_add'
        context['entity'] = 'Dispositivos'
        context['list_url'] = reverse_lazy('sh:device_list')
        context['form_id'] = 'deviceForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['filter_btn_color'] = 'btn-primary'
        context['btn_color'] = 'bg-custom-primary'
        return context

class DeviceUpdateView(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'device/create.html'
    success_url = reverse_lazy('sh:device_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Dispositivo actualizado correctamente',
                    'success': True,
                    'message': 'Switch agregado exitosamente',
                    'device_id': self.object.id,
                    'device_name': f"{self.object.dev_model.dev_type.dev_type} {self.object.dev_model.brand.brand} {self.object.dev_model.dev_model} S/N°: {self.object.serial_n}"
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
            return JsonResponse({'error':errors}, status=400)
        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dispositivos'
        context['title'] = 'Editar Dispositivo'
        context['btn_add_id'] = 'device_add'
        context['entity'] = 'Dispositivos'
        context['list_url'] = reverse_lazy('sh:device_list')
        context['form_id'] = 'deviceForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['filter_btn_color'] = 'bg-custom-warning'
        context['btn_color'] = 'bg-custom-warning'


        device = self.get_object()

        if device.office and device.office.loc and device.office.loc.edifice and device.office.loc.edifice.location and device.office.loc.edifice.location.province and device.office.dependency:

            province = device.office.loc.edifice.location.province
            context['form'].fields['province'].queryset = Province.objects.all()
            context['form'].fields['province'] = province.id

            location = device.office.loc.edifice.location
            context['form'].fields['location'].queryset = Location.objects.filter(province=province)
            context['form'].initial['location'] = location.id

            edifice = device.office.loc.edifice
            context['form'].fields['edifice'].queryset = Edifice.objects.filter(location=location)
            context['form'].initial['edifice'] = edifice.id

            edifice_port = device.office.loc.edifice
            context['form'].fields['edifice_ports'].queryset = Edifice.objects.filter(location=location)
            context['form'].initial['edifice_ports'] = edifice_port

            dependency = device.office.dependency
            context['form'].fields['dependency'].queryset = Dependency.objects.filter(location=location)
            context['form'].initial['dependency'] = dependency.id

            loc = device.office.loc
            context['form'].fields['loc'].queryset = Office_Loc.objects.filter(edifice=edifice)
            context['form'].initial['loc'] = loc.id

            loc_port = device.office.loc
            context['form'].fields['loc_ports'].queryset = Office_Loc.objects.filter(edifice=edifice)
            context['form'].initial['loc_ports'] = loc_port

            office = device.office
            context['form'].fields['office'].queryset = Office.objects.filter(loc=loc)
            context['form'].initial['office'] = office.id

            office_port = device.office
            context['form'].fields['office_ports'].queryset = Office.objects.filter(loc=loc)
            context['form'].initial['office_ports'] = office_port

            wall_port = device.wall_port_in
            context['form'].fields['wall_port_in'].queryset = Wall_Port.objects.filter(office=office)
            context['form'].initial['wall_port_in'] = wall_port

            context['form'].fields['employee'].queryset = Employee.objects.filter(office=office)

            switch_port = device.switch_port_in
            context['form'].fields['switch_port_in'].queryset = Switch_Port.objects.filter(switch__office=office)
            context['form'].initial['switch_port_in'] = switch_port

        return context

class DeviceDeleteView(DeleteView):
    model = Device
    template_name = 'device/delete.html'
    success_url = reverse_lazy('sh:device_list')

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
        context['page_title'] = 'Dispositivos'
        context['title'] = 'Eliminar un Dispositivo'
        context['del_title'] = 'Dispositivo: '
        context['list_url'] = reverse_lazy('sh:device_list')
        context['form_id'] = 'deviceForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context

class DeviceDetailsView(DetailView):
    model = Device
    template_name = 'device/modal_details.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.object
        connections = []
        current = device

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

