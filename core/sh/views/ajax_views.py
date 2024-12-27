from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_http_methods

from core.sh.models.brands.models import Brand
from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.dev_type.models import Dev_Type
from core.sh.models.device.models import Device
from core.sh.models.edifice.models import Edifice
from core.sh.models.employee.models import Employee
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.patch_port.models import Patch_Port
from core.sh.models.patchera.models import Patchera
from core.sh.models.rack.models import Rack
from core.sh.models.switch.models import Switch
from core.sh.models.switch_port.models import Switch_Port
from core.sh.models.wall_port.models import Wall_Port

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_location(request):
    province_id = request.GET.get('province_id') or request.POST.get('province_id')
    locations = Location.objects.all()
    if province_id:
        locations = locations.filter(province_id=province_id)

    data = [{'id': loc.id, 'name': loc.location} for loc in locations]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_dependency(request):
    province_id = request.GET.get('province_id') or request.POST.get('province_id')
    location_id = request.GET.get('location_id') or request.POST.get('location_id')

    dependencies = Dependency.objects.all()
    if province_id:
        dependencies = dependencies.filter(location__province_id=province_id)
    if location_id:
        dependencies = dependencies.filter(location_id=location_id)

    data = [{'id': dep.id, 'name': dep.dependency} for dep in dependencies]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_edifices(request):
    province_id = request.GET.get('province_id') or request.POST.get('province_id')
    location_id = request.GET.get('location_id') or request.POST.get('location_id')

    edifices = Edifice.objects.all()
    if province_id:
        edifices = edifices.filter(location__province_id=province_id)
    if location_id:
        edifices = edifices.filter(location_id=location_id)

    data = [{'id': edif.id, 'name': edif.edifice} for edif in edifices]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_loc(request):
    province_id = request.GET.get('province_id') or request.POST.get('province_id')
    location_id = request.GET.get('location_id') or request.POST.get('location_id')
    edifice_id = request.GET.get('edifice_id') or request.POST.get('edifice_id')

    locs = Office_Loc.objects.all()
    if province_id:
        locs = locs.filter(edifice__location__province_id=province_id)
    if location_id:
        locs = locs.filter(edifice__location_id=location_id)
    if edifice_id:
        locs = locs.filter(edifice_id=edifice_id)

    data = [{'id': l.id, 'name': f'Piso: {l.floor} / Ala: {l.wing}'} for l in locs]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_office(request):
    province_id = request.GET.get('province_id') or request.POST.get('province_id')
    location_id = request.GET.get('location_id') or request.POST.get('location_id')
    dependency_id = request.GET.get('dependency_id') or request.POST.get('dependency_id')
    edifice_id = request.GET.get('edifice_id') or request.POST.get('edifice_id')
    loc_id = request.GET.get('loc_id') or request.POST.get('loc_id')

    filters = {}
    if province_id:
        filters['loc__edifice__location__province_id'] = province_id
    if location_id:
        filters['loc__edifice__location_id'] = location_id
    if edifice_id:
        filters['loc__edifice_id'] = edifice_id
    if dependency_id:
        filters['dependency_id'] = dependency_id
    if loc_id:
        filters['loc_id'] = loc_id

    offices = Office.objects.filter(**filters).distinct()
    data = [{'id': office.id, 'name': str(office.office)} for office in offices]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_rack(request):
    province_id = request.POST.get('province_id')
    location_id = request.POST.get('location_id')
    dependency_id = request.POST.get('dependency_id')
    edifice_id = request.POST.get('edifice_id')
    loc_id = request.POST.get('loc_id')
    office_id = request.POST.get('office_id')

    filters = {}
    if province_id:
        filters['office__loc__edifice__location__province_id']=province_id
    if location_id:
        filters['office__loc__edifice__location_id']=location_id
    if dependency_id:
        filters['office__dependency_id']=dependency_id
    if edifice_id:
        filters['office__loc__edifice_id']=edifice_id
    if loc_id:
        filters['office__loc_id']=loc_id
    if office_id:
        filters['office_id']=office_id

    racks = Rack.objects.filter(**filters).distinct()
    data = [{'id': rack.id, 'name': rack.rack} for rack in racks]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_brand(request):
    usage = request.POST.get('usage')
    dev_type_name = request.POST.get('dev_type_name')

    brands = Brand.objects.all()

    if usage == 'device':
        brands = brands.exclude(models_brand__dev_type__dev_type='SWITCH').distinct()

    elif usage == 'switch':
        brands = brands.filter(models_brand__dev_type__dev_type='SWITCH').distinct()

    if dev_type_name:
        try:
            dev_type_id = int(dev_type_name)
            brands = brands.filter(models_brand__dev_type__id=dev_type_id).distinct()
        except ValueError:
            brands = brands.filter(models_brand__dev_type__dev_type=dev_type_name).distinct()

    data = [{'id': b.id, 'name': b.brand} for b in brands]
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

    if not filters:
        return JsonResponse([], safe=False)

    switches = Switch.objects.filter(**filters).distinct()
    data = [{'id': switch.id, 'name': f"{switch.model.brand.brand} / PUERTOS: {switch.ports_q} / POSICION: {switch.switch_rack_pos}"} for switch in switches]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_patchera(request):
    rack_id = request.POST.get('rack_id')
    patcheras = Patchera.objects.filter(rack_id=rack_id)
    data = [{'id': patch.id, 'name': f'PATCHERA: {patch.patchera}'} for patch in patcheras]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_patch_ports(request):
    """Devuelve los Patch_Port disponibles de una patchera determinada."""
    patchera_id = request.POST.get('patchera_id')
    if not patchera_id:
        return JsonResponse([], safe=False)

    used_ids = set()

    # (a) Patch_Port asignados a Device
    # En Device: patch_port_in = OneToOneField(..., related_name='device_patch_port_in')
    # => inverso: Patch_Port.objects.filter(device_patch_port_in__isnull=False)
    device_patch = Patch_Port.objects.filter(device_patch_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(device_patch)

    # (b) Patch_Port asignados a Switch
    # En Switch: patch_port_in = OneToOneField(..., related_name='switch_patch_port_in')
    # => inverso: Patch_Port.objects.filter(switch_patch_port_in__isnull=False)
    switch_patch = Patch_Port.objects.filter(switch_patch_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(switch_patch)

    # (c) Patch_Port asignados a Wall_Port
    # En Wall_Port: patch_port_in = OneToOneField(..., related_name='wall_patch_port_in')
    # => inverso: Patch_Port.objects.filter(wall_patch_port_in__isnull=False)
    wall_patch = Patch_Port.objects.filter(wall_patch_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(wall_patch)

    # 2. Filtrar los Patch_Port disponibles en la patchera solicitada
    patch_ports = Patch_Port.objects.filter(patchera_id=patchera_id).exclude(id__in=used_ids).order_by('port')

    # 3. Serializar al formato que tu JS espera
    data = [{'id': p.id, 'name': f'Puerto: {p.port}'} for p in patch_ports]
    return JsonResponse(data, safe=False)

# @csrf_protect
# @require_POST
# def ajax_load_patch_ports(request):
#     patchera_id = request.POST.get('patchera_id')

#     used_ports = set()

#     wall_port_used = Wall_Port.objects.exclude(
#         patch_port_in=None
#     ).values_list('patch_port_in_id', flat=True)
#     used_ports.update(wall_port_used)

#     # Puertos usados en Switch
#     switch_used = Switch.objects.exclude(
#         patch_port_in=None
#     ).values_list('patch_port_in_id', flat=True)
#     used_ports.update(switch_used)

#     # Puertos usados en Device
#     device_used = Device.objects.exclude(
#         patch_port_in=None
#     ).values_list('patch_port_in_id', flat=True)
#     used_ports.update(device_used)

#     # Puertos usados en Patchera
#     patchera_used = Patchera.objects.exclude(
#         patch_port_in=None
#     ).values_list('patch_port_in_id', flat=True)
#     used_ports.update(patchera_used)


#     # Si no hay patchera_id, retorna lista vacía
#     if not patchera_id:
#         return JsonResponse([], safe=False)

#     # Filtrar puertos disponibles
#     patch_ports = Patch_Port.objects.filter(
#         patchera_id=patchera_id
#     ).exclude(
#         id__in=list(used_ports)
#     ).order_by('port')

#     data = [{
#         'id': p.id,
#         'name': f'Puerto: {p.port}'
#     } for p in patch_ports]

#     return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_model(request):
    usage = request.POST.get('usage')
    dev_type_name = request.POST.get('dev_type_name')
    brand_id = request.POST.get('brand_id')

    dev_models = Dev_Model.objects.all()

    if usage == 'device':
        dev_models = dev_models.exclude(dev_type__dev_type='SWITCH')
    elif usage == 'switch':
        dev_models = dev_models.filter(dev_type__dev_type='SWITCH')

    if brand_id and brand_id.strip():
        try:
            brand_id_int = int(brand_id)
            dev_models = dev_models.filter(brand_id=brand_id_int)
        except ValueError:
            dev_models = dev_models.none()

    if dev_type_name and dev_type_name.strip():
        try:
            dev_type_id = int(dev_type_name)
            dev_models = dev_models.filter(dev_type_id=dev_type_id)
        except ValueError:
            dev_models = dev_models.filter(dev_type__dev_type=dev_type_name)

    dev_models = dev_models.distinct()

    data = [{'id': m.id, 'name': m.dev_model} for m in dev_models]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_wall_port(request):

    office_id = request.POST.get('office_id')
    print ('Office ID:', office_id)
    if not office_id:
        return JsonResponse([], safe=False)

    used_ids = set()

    device_wall = Wall_Port.objects.filter(device_wall_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(device_wall)

    switch_wall = Wall_Port.objects.filter(switch_wall_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(switch_wall)

    wall_ports = Wall_Port.objects.filter(office_id=office_id).exclude(id__in=used_ids).order_by('wall_port')
    print('Wall Ports:', list(wall_ports.values_list('id', 'wall_port')))

    data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]
    return JsonResponse(data, safe=False)

# @csrf_protect
# @require_POST
# def ajax_load_wall_port(request):
#     office_id = request.POST.get('office_id')
#     if not office_id:
#         return JsonResponse([], safe=False)

#     used_ports = set()

#     device_wall_port_in = Wall_Port.objects.filter(device_wall_port_in__isnull=False).values_list('id', flat=True)
#     used_ports.update(device_wall_port_in)

#     switch_wall_port_in = Wall_Port.objects.filter(switch_port_in__isnull=False).values_list('id', flat=True)
#     used_ports.update(switch_wall_port_in)

#     patch_wall_port_in = Wall_Port.objects.filter(patch_port_in__isnull=False).values_list('id', flat=True)
#     used_ports.update(patch_wall_port_in)

#     wall_ports = Wall_Port.objects.filter(office_id=office_id).exclude(id__in=used_ports)

#     data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]
#     return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_switch_port(request):
    switch_id = request.POST.get('switch_id')

    used_ports = set()

    wall_port_used = Wall_Port.objects.exclude(
        switch_port_in=None
        ).values_list('switch_port_in_id', flat=True)
    used_ports.update(wall_port_used)

    switch_used = Switch.objects.exclude(
        switch_port_in=None
        ).values_list('switch_port_in_id', flat=True)
    used_ports.update(switch_used)

    device_used = Device.objects.exclude(
        switch_port_in=None
        ).values_list('patch_port_in_id', flat=True)
    used_ports.update(device_used)

    if not switch_id:
        return JsonResponse([], safe=False)

    switch_ports = Switch_Port.objects.filter(
        switch_id=switch_id
        ).exclude(
            id__in=list(used_ports)
    ).order_by('port_id')

    data=[{
        'id': sp.id,
        'name': f'Puerto: {sp.port_id}'
    } for sp in switch_ports]

    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_employee(request):
    office_id = request.POST.get('office_id')
    employees = Employee.objects.filter(office_id=office_id)
    data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_dev_type(request):
    usage = request.POST.get('usage', '')
    dev_types = Dev_Type.objects.all()

    if usage == 'device':
        dev_types = dev_types.exclude(dev_type='SWITCH')
    elif usage == 'switch':
        dev_types = dev_types.filter(dev_type='SWITCH')

    data = [{'id': dt.id, 'name': dt.dev_type} for dt in dev_types]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_province_location(request):
    office_id = request.POST.get('office_id')
    print(f"ajax_load_province_location - office_id recibido: {office_id}")
    if not office_id:
        return JsonResponse({'error': 'No office_id provided'}, status=400)

    try:
        office = Office.objects.select_related('loc__edifice__location').get(id=office_id)
        location = office.loc.edifice.location
        province = location.province

        print(f"ajax_load_province_location - location_id: {location.id} - province_id: {province.id}")

        return JsonResponse({
            'province_id': province.id,
            'province_name': province.province,
            'location_id': location.id,
            'location_name': location.location,
        })
    except Office.DoesNotExist:
        return JsonResponse({'error': 'Office not found'}, status=404)
