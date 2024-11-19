from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from core.sh.models import (
    Dependency, Dev_Model, Edifice, Employee, Location,
    Office, Office_Loc, Switch_Port, Wall_Port, Rack, Switch,
    Patchera, Patch_Port
)

@csrf_protect
@require_POST
def ajax_load_location(request):
    province_id = request.POST.get('province_id')
    locations = Location.objects.filter(province_id=province_id)
    data = [{'id': loc.id, 'name': loc.location} for loc in locations]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_dependency(request):
    location_id = request.POST.get('location_id')
    dependencies = Dependency.objects.filter(edifice__location_id=location_id).distinct()
    data = [{'id': dep.id, 'name': dep.dependency} for dep in dependencies]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_edifices(request):
    location_id = request.POST.get('location_id')
    edifices = Edifice.objects.filter(location_id=location_id)
    data = [{'id': edif.id, 'name': edif.edifice} for edif in edifices]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_loc(request):
    edifice_id = request.POST.get('edifice_id')
    locs = Office_Loc.objects.filter(edifice_id=edifice_id)
    data = [{'id': loc.id, 'name': f'Piso: {loc.floor} / Ala: {loc.wing}'} for loc in locs]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_office(request):
    loc_id = request.POST.get('loc_id')
    offices = Office.objects.filter(loc_id=loc_id)
    data = [{'id': office.id, 'name': office.office} for office in offices]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_rack(request):
    office_id = request.POST.get('office_id')
    racks = Rack.objects.filter(office_id=office_id)
    data = [{'id': rack.id, 'name': rack.name} for rack in racks]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_switch(request):
    office_id = request.POST.get('office_id')
    rack_id = request.POST.get('rack_id')
    filters = {}
    if office_id:
        filters['office_id'] = office_id
    if rack_id:
        filters['rack_id'] = rack_id
    switches = Switch.objects.filter(**filters).distinct()
    data = [{'id': switch.id, 'name': switch.name} for switch in switches]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_patchera(request):
    rack_id = request.POST.get('rack_id')
    patcheras = Patchera.objects.filter(rack_id=rack_id)
    data = [{'id': patchera.id, 'name': patchera.name} for patchera in patcheras]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_patch_ports(request):
    patchera_id = request.POST.get('patchera_id')
    patch_ports = Patch_Port.objects.filter(patchera_id=patchera_id)
    data = [{'id': port.id, 'name': port.port_number} for port in patch_ports]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_model(request):
    def to_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    brand_id = to_int(request.POST.get('brand_id'))
    dev_type_id = to_int(request.POST.get('dev_type_id'))

    filters = {}
    if brand_id is not None:
        filters['brand_id'] = brand_id
    if dev_type_id is not None:
        filters['dev_type_id'] = dev_type_id

    models = Dev_Model.objects.filter(**filters).distinct()
    data = [{'id': model.id, 'name': model.dev_model} for model in models]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_wall_port(request):
    office_id = request.POST.get('office_id')
    wall_ports = Wall_Port.objects.filter(office_id=office_id)
    data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_switch_port(request):
    office_id = request.POST.get('office_id')
    switch_ports = Switch_Port.objects.filter(switch__office_id=office_id)
    data = [{'id': s.id, 'name': f'Puerto: {s.port_id}, Switch: {s.switch}'} for s in switch_ports]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_employee(request):
    office_id = request.POST.get('office_id')
    employees = Employee.objects.filter(office_id=office_id)
    data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]
    return JsonResponse(data, safe=False)
