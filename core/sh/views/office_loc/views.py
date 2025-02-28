from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms import Office_Loc_Form
from core.sh.forms.edifice.forms import EdificeForm
from core.sh.forms.location.forms import LocationForm
from core.sh.forms.modals.forms import ProvinceModalForm
from core.sh.forms.province.forms import ProvinceForm
from core.sh.models import Edifice, Location, Office_Loc, Province

class Office_Loc_ListView(ListView):
    model = Office_Loc
    template_name = 'office_loc/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'searchdata':
                office_locs = Office_Loc.objects.all()
                data = [ol.toJSON() for ol in office_locs]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ubicaciónes de Oficinas'
        context['title'] = 'Ubicación de Oficina'
        context['btn_add_id'] = 'office_loc_add'
        context['create_url'] = reverse_lazy('sh:office_loc_add')
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['entity'] = 'Ubicación de Oficina'
        context['nav_icon'] = 'fa-solid fa-building'
        context['table_id'] = 'office_loc_table'
        context['add_btn_title'] = 'Agregar Ubicación de Oficina'
        return context

class Office_Loc_CreateView(CreateView):
    model = Office_Loc
    form_class = Office_Loc_Form
    template_name = "office_loc/create.html"
    success_url = reverse_lazy('sh:office_loc_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Ubicación de oficina agregada correctamente',
                    'office_loc_id': self.object.id,
                    'office_loc_edifice': self.object.edifice.edifice,
                    'office_loc_floor': self.object.floor,
                    'office_loc_wing': self.object.wing,
                    'loc_name': f" PISO: {self.object.floor} / ALA: {self.object.wing} "
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
        context['page_title'] = 'Ubicaciónes de Oficinas'
        context['title'] = 'Agregar una Ubicación de Oficina'
        context['btn_add_id'] = 'office_loc_add'
        context['entity'] = 'Ubicación de Oficina'
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['form_id'] = 'office_locForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['edifice_add'] = EdificeForm()
        context['location_add'] = LocationForm()
        context['province_add'] = ProvinceForm()
        context['province_modal_add'] = ProvinceModalForm()
        context['btn_color'] = 'btn-primary'
        context['filter_btn_color'] = 'btn-primary'
        return context

class Office_Loc_UpdateView(UpdateView):
    model = Office_Loc
    form_class = Office_Loc_Form
    template_name = "office_loc/create.html"
    success_url = reverse_lazy('sh:office_loc_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Ubicación de oficina actualiza correctamente',
                    'loc_id': self.object.id,
                    'loc_edifice': self.object.edifice.edifice,
                    'loc_floor': self.object.floor,
                    'loc_wing': self.object.wing,
                    'loc_name': f" PISO: {self.object.floor} / ALA: {self.object.wing} "
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
        context['page_title'] = 'Ubicaciónes de Oficinas'
        context['title'] = 'Editar Ubicación de Oficina'
        context['btn_add_id'] = 'office_loc_add'
        context['entity'] = 'Ubicación de Oficina'
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['form_id'] = 'office_locForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['edifice_add'] = EdificeForm()
        context['location_add'] = LocationForm()
        context['province_add'] = ProvinceForm()
        context['btn_color'] = 'bg-custom-warning'
        context['filter_btn_color'] = 'bg-custom-warning'

        office_loc = self.get_object()

        if office_loc.edifice and office_loc.edifice.location and office_loc.edifice.location.province:
            context['form'].initial['province'] = office_loc.edifice.location.province.id
            context['form'].initial['location'] = office_loc.edifice.location.id if office_loc.edifice.location else None
            context['form'].initial['edifice'] = office_loc.edifice.id if office_loc.edifice else None
            context['form'].fields['province'].widget.attrs.update({
                'data-preselected': self.object.edifice.location.province.id if self.object.edifice.location and self.object.edifice.location.province else '',
            })
            context['form'].fields['location'].widget.attrs.update({
                'data-preselected': self.object.edifice.location.id if self.object.edifice.location else '',
            })
            return context

class Office_Loc_DeleteView(DeleteView):
    model = Office_Loc
    template_name = 'office_loc/delete.html'
    success_url = reverse_lazy('sh:office_loc_list')

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
        context['page_title'] = 'Ubicaciónes de Oficinas'
        context['title'] = 'Eliminar una Locaión de Oficina'
        context['del_title'] = 'Ubicación de Oficina: '
        context['list_url'] = reverse_lazy('sh:office_loc_list')
        context['form_id'] = 'office_locForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context