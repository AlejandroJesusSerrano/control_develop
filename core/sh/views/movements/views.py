from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
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
            elif action == 'get-details':
                movement_id = request.POST.get('id')
                movement = Movements.objects.get(id=movement_id)
                data = movement.toJSON()
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
        context['add_btn_title'] = 'Agregar Movimiento'
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

    def form_valid(self, form):

        try:

            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Movimiento guardado correctamente'
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
        context['page_title'] = 'Movimientos'
        context['title'] = 'Agregar un Movimiento'
        context['btn_add_id'] = 'move_add'
        context['entity'] = 'Movimientos'
        context['list_url'] = self.success_url
        context['form_id'] = 'MovementsForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['filter_btn_color'] = 'btn-primary'
        context['btn_color'] = 'bg-custom-primary'
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

    def form_valid(self, form):
        try:

            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Dispositivo actualizado correctamente'
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
        context['page_title'] = 'Movimientos'
        context['title'] = 'Editar Movimiento'
        context['btn_add_id'] = 'move_add'
        context['entity'] = 'Movimientos'
        context['list_url'] = reverse_lazy('sh:move_list')
        context['form_id'] = 'MovementsForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['filter_btn_color'] = 'btn-warning'
        context['btn_color'] = 'bg-custom-warning'
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
        context['btn_color'] = 'bg-custom-danger'
        return context

class MovementsDetailsView(DetailView):
    model = Movements
    template_name = 'Movements/modal_details.html'
    context_object_name = 'movement'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print("Objeto:", self.object)
        print("Detalle:", self.object.detail)  # This line is not working
        context = self.get_context_data(object=self.object)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, self.template_name, context)
        else:
            return super().get(request, *args, **kwargs)
