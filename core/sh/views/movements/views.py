from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from core.sh.forms.movements.forms import MovementsForm
from core.sh.models.movements.models import Movements


class MovementsListView(ListView):
    model = Movements
    template_name = 'Movements/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'searchdata':
                movements = Movements.objects.all()
                data = [m.toJSON() for m in movements]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movimientos'
        context['title'] = 'Listado de Movimientos'
        context['btn_add_id'] = 'move_add'
        context['create_url'] = reverse_lazy('sh:move_add')
        context['list_url'] = reverse_lazy('sh:move_list')
        context['entity'] = 'Movimientos'
        context['nav_icon'] = 'fa-regular fa-building'
        context['table_id'] = 'movement_table'
        return context

# core/sh/views/movements/views.py
class MovementsCreateView(CreateView):
    model = Movements
    form_class = MovementsForm
    template_name = 'Movements/create.html'
    success_url = reverse_lazy('sh:move_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    # 1) Guardar el Movement
                    movement = form.save(commit=False)
                    movement.save()

                    # 2) (Opcional) Reasignar la oficina del Device
                    if movement.device and movement.office:
                        movement.device.office = movement.office
                        movement.device.save()

                    # 3) (Opcional) Reasignar el "empleado" al device
                    # ojo que device.employee es ManyToMany
                    if movement.device and movement.employee:
                        movement.device.employee.clear()  # limpiar M2M
                        movement.device.employee.add(movement.employee)
                        movement.device.save()

                    data['success'] = True
                else:
                    data['errors'] = form.errors
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movimientos'
        context['title'] = 'Agregar un Movimiento'
        context['btn_add_id'] = 'move_add'
        context['entity'] = 'Movimientos'
        context['list_url'] = self.success_url
        context['form_id'] = 'MovementsForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['filter_btn_color'] = 'btn-primary'
        return context

class MovementsUpdateView(UpdateView):
    model = Movements
    form_class = MovementsForm
    template_name = 'Movements/create.html'
    success_url = reverse_lazy('sh:move_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    data['success'] = True
                else:
                    data['errors'] = form.errors
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movimientos'
        context['title'] = 'Editar Movimiento'
        context['btn_add_id'] = 'move_add'
        context['entity'] = 'Movimientos'
        context['list_url'] = reverse_lazy('sh:move_list')
        context['form_id'] = 'MovementsForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        return context


class MovementsDeleteView(DeleteView):
    model = Movements
    template_name = 'Movements/delete.html'
    success_url = reverse_lazy('sh:move_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
            data['success'] = True
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Movimientos'
        context['title'] = 'Eliminar un Movimiento'
        context['del_title'] = 'Movimiento: '
        context['list_url'] = reverse_lazy('sh:move_list')
        context['form_id'] = 'MovementsForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context