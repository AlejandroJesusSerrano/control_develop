from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from core.sh.forms.move_type.forms import MoveTypeForm
from core.sh.models.move_type.models import Move_Type


class Move_Type_ListView(ListView):
    model = Move_Type
    template_name='move_type/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Move_Type.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tipos de Movimientos'
        context['title'] = 'Listado de Tipos de Movimientos'
        context['btn_add_id'] = 'move_type_add'
        context['create_url'] = reverse_lazy('sh:move_type_add')
        context['list_url'] = reverse_lazy('sh:move_type_list')
        context['entity'] = 'Tipos de Movimientos'
        context['nav_icon'] = 'fa-solid fa-arrows-turn-to-dots'
        context['table_id'] = 'move_type_table'
        context['add_btn_title'] = 'Agregar Tipo de Movimiento'
        return context

class Move_Type_CreateView(CreateView):
    model = Move_Type
    form_class = MoveTypeForm
    template_name = 'move_type/create.html'
    success_url = reverse_lazy('sh:move_type_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return ['move_type/popup_add.html']
        return ['move_type/create.html']

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Ubicación de oficina agregada correctamente',
                    'move_type_id': self.object.id,
                    'move_type_name': self.object.move,
                    'move_type_details': self.object.details
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
        context['page_title'] = 'Tipos de Movimientos'
        context['title'] = 'Agregar una Tipo de Movimiento'
        context['btn_add_id'] = 'move_t_add'
        context['entity'] = 'Tipos de Movimientos'
        context['list_url'] = reverse_lazy('sh:move_type_list')
        context['form_id'] = 'move_tForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        return context

class Move_Type_UpdateView(UpdateView):
    model = Move_Type
    form_class = MoveTypeForm
    template_name = 'move_type/create.html'
    success_url = reverse_lazy('sh:move_type_list')

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
                    'message': 'Ubicación de oficina actualiza correctamente',
                    'move_type_id': self.object.id,
                    'move_type_name': self.object.move,
                    'move_type_details': self.object.details
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
        context['page_title'] = 'Tipos de Movimientos'
        context['title'] = 'Editar Datos de una Tipo de Movimiento'
        context['btn_add_id'] = 'move_t_add'
        context['entity'] = 'Tipos de Movimientos'
        context['list_url'] = reverse_lazy('sh:move_type_list')
        context['form_id'] = 'move_tForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        return context

class Move_Type_DeleteView(DeleteView):
    model = Move_Type
    template_name = 'move_type/delete.html'
    success_url = reverse_lazy('sh:move_type_list')

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
        context['page_title'] = 'Tipos de Movimientos'
        context['title'] = 'Eliminar una Tipo de Movimiento'
        context['del_title'] = 'Tipo de Movimiento: '
        context['list_url'] = reverse_lazy('sh:move_type_list')
        context['form_id'] = 'move_tForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context
