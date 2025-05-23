from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from core.sh.forms import EmployeeForm
from core.sh.models.dependency.models import Dependency
from core.sh.models.edifice.models import Edifice
from core.sh.models.employee.models import Employee
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.province.models import Province

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post (self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Employee.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Empleados'
        context['title'] = 'Listado de Empleados'
        context['btn_add_id'] = 'employee_add'
        context['create_url'] = reverse_lazy('sh:employee_add')
        context['list_url'] = reverse_lazy('sh:employee_list')
        context['entity'] = 'Empleados'
        context['nav_icon'] = 'fa fa-user-tie'
        context['table_id'] = 'employee_table'
        context['add_btn_title'] = 'Agregar Empleado'
        return context

class EmployeeCreateView(CreateView):
    model: Employee
    form_class = EmployeeForm
    template_name = 'employee/create.html'
    success_url = reverse_lazy('sh:employee_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.GET.get('popup') == '1':
            return ['employee/popup_add.html']
        return ['employee/create.html']

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Empleado agregado correctamente',
                    'employee_id': self.object.id,
                    'employee_name': f"{self.object.employee_last_name}, {self.object.employee_name}"
                }
                return JsonResponse(data)
            else:
                return super().form_valid(form)
        except Exception as e:
            if self.request.headers.get('x-reuquested-with') == 'XMLHttpRequest':
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
        context['page_title'] = 'Empleados'
        context['title'] = 'Agregar un Empleado'
        context['btn_add_id'] = 'employee_add'
        context['entity'] = 'Empleados'
        context['list_url'] = reverse_lazy('sh:employee_list')
        context['form_id'] = 'employeeForm'
        context['action'] = 'add'
        context['bg_color'] = 'bg-custom-primary'
        context['btn_color'] = 'bg-custom-primary'
        context['filter_btn_color'] = 'bg-custom-primary'
        return context

class EmployeeUpadateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/create.html'
    success_url = reverse_lazy('sh:employee_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()

            if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Empleado actualizado correctamente',
                    'employee_id': self.object.id,
                    'employee_name': f"{self.object.employee_last_name}, {self.object.employee_name}"
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
        context['page_title'] = 'Empleados'
        context['title'] = 'Editar Empleado'
        context['btn_add_id'] = 'employee_add'
        context['entity'] = 'Empleados'
        context['list_url'] = reverse_lazy('sh:employee_list')
        context['form_id'] = 'employeeForm'
        context['action'] = 'edit'
        context['bg_color'] = 'bg-custom-warning'
        context['filter_btn_color'] = 'bg-custom-warning'

        employee = self.get_object()

        if employee.office and employee.office.loc and employee.office.loc.edifice:
            context['form'].fields['edifice'].queryset = Edifice.objects.filter(
                location=employee.office.loc.edifice.location
        )

        if employee.office:
            context['form'].fields['office'].queryset = Office.objects.select_related('loc__edifice').filter(
                loc__edifice=employee.office.loc.edifice
        )

        if employee.office and employee.office.loc and employee.office.loc.edifice:
            context['form'].initial['location'] = employee.office.loc.edifice.location.id
            context['form'].initial['edifice'] = employee.office.loc.edifice.id
            context['form'].initial['office'] = employee.office.id if employee.office else None

        context['form'].fields['edifice'].widget.attrs.update({
            'data-preselected': self.object.office.loc.edifice.id if self.object.office.loc.edifice else ''
        })
        context['form'].fields['office'].widget.attrs.update({
            'data-preselected': self.object.office.id if self.object.office else ''
        })

        return context

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee/delete.html'
    success_url = reverse_lazy('sh:employee_list')

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
        context['page_title'] = 'Empleados'
        context['title'] = 'Eliminar una Empleado'
        context['del_title'] = 'Empleado: '
        context['list_url'] = reverse_lazy('sh:employee_list')
        context['form_id'] = 'employeeForm'
        context['bg_color'] = 'bg-custom-danger'
        context['action'] = 'delete'
        return context

class EmployeeDetailsView(DetailView):
    model = Employee
    template_name = 'employee/modal_details.html'
    context_object_name = 'employee'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render (request, self.template_name, context)
        return super().get(request, *args, **kwargs)