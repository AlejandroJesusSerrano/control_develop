from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator


from core.sh.forms.switch_font.forms import SwitchFontForm
from core.sh.models.switch_font.models import SwitchFont


class SwitchFontListView(ListView):
    model = SwitchFont
    template_name = 'switch_font/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                switches = SwitchFont.objects.all()
                data = [s.toJSON() for s in switches]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Fuentes de Switchs'
        context['title'] = 'Listado de Fuentes de Switchs'
        context['btn_add_id'] = 'switch_font_add'
        context['create_url'] = reverse_lazy('sh:switch_font_add')
        context['list_url'] = reverse_lazy('sh:switch_font_list')
        context['entity'] = 'Fuente de Switch'
        context['nav_icon'] = 'fa fa-copyright'
        context['table_id'] = 'switch_font_table'
        context['add_btn_title'] = 'Agregar Fuente de Switch'
        return context

class SwitchFontCreateView(CreateView):
    model = SwitchFont
    form_class = SwitchFontForm
    template_name = 'switch_font/create.html'
    success_url = reverse_lazy('sh:switch_font_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Fuente de Switch agregada exitosamente',
                    'font_id': self.object.id,
                    'font_name': self.object.font_name,
                    'switch': f'{self.object.switch.model.brand.brand} {self.object.switch.model.dev_model} DE {self.object.switch.ports_q} PUERTOS',
                    'font_status': self.object.font_status,
                    'send_date': self.object.send_date.stfrtime('%d/%m/%Y') if self.object.send_date else 'NO TIENE FECHA DE ENVIO',
                    'reception_date': self.object.reception_date.strftime('%d/%m/%Y') if self.object.reception_date else 'NO TIENE FECHA DE RECEPCION',
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
        context['page_title'] = 'Fuentes de Switchs'
        context['title'] = 'Agregar una Fuente de Switch'
        context['btn_add_id'] = 'switch_font_add'
        context['entity'] = 'Fuente de Switch'
        context['list_url'] = reverse_lazy('sh:switch_font_list')
        context['form_id'] = 'switchFontForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['filter_btn_color'] = 'btn-primary'
        context['dev_type_id'] = 'SWITCH FONT'
        context['btn_color'] = 'btn-primary'
        return context

class SwitchFontUpdateView(UpdateView):
    model = SwitchFont
    form_class = SwitchFontForm
    template_name = 'switch_font/create.html'
    success_url = reverse_lazy('sh:switch_font_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Fuente de Switch agregada exitosamente',
                    'font_name': self.object.id,
                    'switch': f'{self.object.switch.model.brand.brand} {self.object.switch.model.dev_model} DE {self.object.switch.ports_q} PUERTOS',
                    'font_status': self.object.font_status,
                    'send_date': self.object.send_date.stfrtime('%d/%m/%Y') if self.object.send_date else 'NO TIENE FECHA DE ENVIO',
                    'reception_date': self.object.reception_date.strftime('%d/%m/%Y') if self.object.reception_date else 'NO TIENE FECHA DE RECEPCION',
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
        context['switch_id'] = self.object.id
        context['page_title'] = 'Fuentes de Switchs'
        context['title'] = 'Editar una Fuente de Switch'
        context['btn_add_id'] = 'switch_font_add'
        context['entity'] = 'Fuente de Switch'
        context['list_url'] = reverse_lazy('sh:switch_font_list')
        context['form_id'] = 'switchFontForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['filter_btn_color'] = 'bg-custom-warning'
        context['btn_color'] = 'bg-custom-warning'

        return context

class SwitchFontDeleteView(DeleteView):
    model = SwitchFont
    template_name = 'switch_font/delete.html'
    success_url = reverse_lazy('sh:switch_font_list')

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
        context['page_title'] = 'Switchs'
        context['title'] = 'Eliminar un Switch'
        context['del_title'] = 'Switch: '
        context['list_url'] = reverse_lazy('sh:switch_list')
        context['form_id'] = 'switchForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context