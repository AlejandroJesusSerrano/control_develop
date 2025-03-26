from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_http_methods
from django.db import models
from django.db.models import Q

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

        try:
            province_id = int(province_id)
            locations = locations.filter(province_id=province_id)
        except ValueError:
            return JsonResponse([], safe=False)

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
    data = [{
        'id': office.id,
        'name': f'PROVINCIA: {office.loc.edifice.location.province.province} / LOCALIDAD: {office.loc.edifice.location.location} / DEPENDENCIA: {office.dependency.dependency} / OFICINA: {office.office}'
        } for office in offices]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_rack(request):

    racks = Rack.objects.all()

    province_id = request.POST.get('province_id')
    location_id = request.POST.get('location_id')
    dependency_id = request.POST.get('dependency_id')
    edifice_id = request.POST.get('edifice_id')
    loc_id = request.POST.get('loc_id')
    office_id = request.POST.get('office_id')

    if province_id:
        racks = racks.filter(office__loc__edifice__location__province_id=province_id)
    if location_id:
        racks = racks.filter(office__loc__edifice__location_id=location_id)
    if dependency_id:
        racks = racks.filter(office__dependency_id=dependency_id)
    if edifice_id:
        racks = racks.filter(office__loc__edifice_id=edifice_id)
    if loc_id:
        racks = racks.filter(office__loc_id=loc_id)
    if office_id:
        racks = racks.filter(office_id=office_id)

    data = [{'id': rack.id, 'name': f'RACK: {rack.rack} EN OFICINA: {rack.office.office}'} for rack in racks]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_switch_rack_pos(request):
    rack_id = request.POST.get('rack_id')
    office_id = request.POST.get('office_id')

    qs = Switch.objects.all()
    if office_id:
        qs = qs.filter(office_id=office_id)
    if rack_id:
        qs = qs.filter(rack_id=rack_id)

    positions = qs.values_list('switch_rack_pos', flat=True).distinct()
    data = [{'id': pos, 'name': pos} for pos in positions if pos]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_brand(request):

    try:
        usage = request.POST.get('usage')
        dev_type_name = request.POST.get('dev_type_name')
        office_id = request.POST.get('office_id')

        brands = Brand.objects.all()

        # 1) Filtrar si usage=device => no ver SWITCH, y viceversa
        if usage == 'device':
            brands = brands.exclude(models_brand__dev_type__dev_type='SWITCH').distinct()
        elif usage == 'switch':
            brands = brands.filter(models_brand__dev_type__dev_type='SWITCH').distinct()

        # 2) Filtrar por dev_type_name si existe
        if dev_type_name:
            try:
                dev_type_id = int(dev_type_name)
                brands = brands.filter(models_brand__dev_type_id=dev_type_id).distinct()
            except ValueError:
                brands = brands.filter(models_brand__dev_type__dev_type=dev_type_name).distinct()

        # 3) Filtrar por office si corresponde
        if office_id:
            # Filtra Brand -> Dev_Model -> Device y Brand -> Dev_Model -> Switch
            # Unimos los dos con Q
            from django.db.models import Q
            brands = brands.filter(
                Q(models_brand__device_model__office_id=office_id) |
                Q(models_brand__switch_model__office_id=office_id)
            ).distinct()

        data = [{'id': b.id, 'name': b.brand} for b in brands]
        return JsonResponse(data, safe=False)

    except Exception as e:
        print(f"Error en ajax_load_brand: {e}")
        return JsonResponse({'error': f'Error en servidor: {str(e)}'}, status=500)

@csrf_protect
@require_POST
def ajax_load_device(request):

    office_id = request.POST.get('office_id')

    devices = Device.objects.exclude(dev_model__dev_type__dev_type='SWITCH')

    if office_id:
        devices = devices.filter(office_id=office_id).distinct()

    data = [
        {
            'id': d.id,
            'name': str(f"\u2022 DISPOSITIVO: {d.dev_model.dev_type.dev_type} / MODELO: {d.dev_model} / SERIAL N°: {d.serial_n} / IP: {d.ip} / USUARIO: {d.employee} / HOSTNAME: {d.net_name}")
        } for d in devices
    ]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_switch(request):

    switches = Switch.objects.all()

    location_id = request.POST.get('location_id') or request.GET.get('location_id')
    office_id = request.POST.get('office_id') or request.GET.get('office_id')
    rack_id = request.POST.get('rack_id') or request.GET.get('rack_id')
    exclude_switch_id = request.POST.get('exclude_switch_id') or request.GET.get('exclude_switch_id')

    filters = {}

    if location_id:
        try:
            filters['office__loc__edifice__location_id'] = location_id
        except ValueError:
            print('Error en location_id:', location_id)

    if office_id:
        try:
            filters['office_id'] = office_id
        except ValueError:
            print('Error en office_id:', office_id)

    if rack_id:
        try:
            filters['rack_id'] = rack_id
        except ValueError:
            print('Error en rack_id:', rack_id)


    if not filters:
        switches = Switch.objects.all()
    else:
        switches = Switch.objects.filter(**filters).distinct()

    if exclude_switch_id:
        try:
            switches = switches.exclude(id=int(exclude_switch_id))
        except ValueError:
            print('Error en exclude_switch_id:', exclude_switch_id)

    data = [

        {
            'id': switch.id,
            'name': f"{switch.model.brand.brand} / PUERTOS: {switch.ports_q} / POSICION: {switch.switch_rack_pos}"
        } for switch in switches

    ]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_ip(request):
    usage = request.POST.get('usage')
    dev_type_name = request.POST.get('dev_type_name')
    office_id = request.POST.get('office_id')

    devices = Device.objects.all()
    if office_id:
        devices = devices.filter(office_id=office_id)

    if usage == 'device':
        devices = devices.exclude(dev_model__dev_type__dev_type='SWITCH')
    elif usage == 'switch':
        devices = devices.filter(dev_model__dev_type__dev_type='SWITCH')

    if dev_type_name:
        try:
            dev_type_id = int(dev_type_name)
            devices = devices.filter(dev_model__dev_type_id=dev_type_id)
        except ValueError:
            devices = devices.filter(dev_model__dev_type__dev_type=dev_type_name)

    ips = devices.values_list('ip', flat=True).distinct()
    data = [{'id': ip, 'name': ip} for ip in ips if ip]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def load_device_serial_n(request):
    brand_id = request.POST.get('brand_id')
    dev_type_name = request.POST.get('dev_type_name')
    office_id = request.POST.get('office_id')

    devices = Device.objects.all()
    if brand_id:
        devices = devices.filter(dev_model__brand_id=brand_id)
    if dev_type_name:
        try:
            dev_type_id = int(dev_type_name)
            devices = devices.filter(dev_model__dev_type_id=dev_type_id)
        except ValueError:
            devices = devices.filter(dev_model__dev_type__dev_type=dev_type_name)
    if office_id:
        devices = devices.filter(office_id=office_id)

    serial_n = devices.values_list('serial_n', flat=True).distinct()
    data = [{'id': sn, 'name': sn} for sn in serial_n if sn]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def load_switch_serial_n(request):
    brand_id = request.POST.get('brand_id')
    office_id = request.POST.get('office_id')

    switches = Switch.objects.all()
    if brand_id:
        switches = switches.filter(model__brand_id=brand_id)
    if office_id:
        switches = switches.filter(office_id=office_id)

    serial_n = switches.values_list('serial_n', flat=True).distinct()
    data = [{'id': sn, 'name': sn} for sn in serial_n if sn]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_patchera(request):
    patcheras = Patchera.objects.all()

    filters = {}

    location_id = request.POST.get('location_id') or request.GET.get('location_id')
    office_id = request.POST.get('office_id') or request.GET.get('office_id')
    rack_id = request.POST.get('rack_id') or request.GET.get('rack_id')

    if location_id:
        patcheras = patcheras.filter(rack__office__loc__edifice__location_id=location_id)
    if office_id:
        patcheras = patcheras.filter(rack__office_id=office_id)
    if rack_id:
        patcheras = patcheras.filter(rack_id=rack_id)

    if not filters:
        patcheras = Patchera.objects.all()
    else:
        patcheras = Patchera.objects.filter(**filters).distinct()

    data = [
        {
            'id': patch.id,
            'name': f'PATCHERA: {patch.patchera} / RACK: {patch.rack.rack}'
        } for patch in patcheras
    ]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_patch_ports(request):

    patchera_id = request.POST.get('patchera_id') or request.GET.get('patchera_id')

    used_ids = set()

    device_patch = Patch_Port.objects.filter(device_patch_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(device_patch)

    switch_patch = Patch_Port.objects.filter(switch_patch_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(switch_patch)

    wall_patch = Patch_Port.objects.filter(wall_patch_port_in__isnull=False).values_list('id', flat=True)
    used_ids.update(wall_patch)

    if not patchera_id:
        patch_ports = Patch_Port.objects.exclude(id__in=used_ids).order_by('port')
    else:
        patch_ports = Patch_Port.objects.filter(patchera_id=patchera_id).exclude(id__in=used_ids).order_by('port')

    data = [{'id': p.id, 'name': f'Puerto: {p.port}'} for p in patch_ports]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_model(request):
    """
    Carga Dev_Model segun usage (device/switch).
    Filtra brand, dev_type y office (buscando Device u Switch).
    """
    usage = request.POST.get('usage')  # 'device' o 'switch'
    dev_type_name = request.POST.get('dev_type_name')
    brand_id = request.POST.get('brand_id')
    office_id = request.POST.get('office_id')

    dev_models = Dev_Model.objects.all()

    # 1) Filtrar usage
    if usage == 'device':
        dev_models = dev_models.exclude(dev_type__dev_type='SWITCH')
    elif usage == 'switch':
        dev_models = dev_models.filter(dev_type__dev_type='SWITCH')

    # 2) Filtrar brand
    if brand_id and brand_id.strip():
        try:
            brand_id_int = int(brand_id)
            dev_models = dev_models.filter(brand_id=brand_id_int)
        except ValueError:
            dev_models = dev_models.filter(brand__brand=brand_id)

    # 3) Filtrar dev_type_name
    if dev_type_name and dev_type_name.strip():
        try:
            dev_type_id = int(dev_type_name)
            dev_models = dev_models.filter(dev_type_id=dev_type_id)
        except ValueError:
            dev_models = dev_models.filter(dev_type__dev_type=dev_type_name)

    # 4) Filtrar por office
    if office_id:
        # Device => device_model
        # Switch => switch_model
        # Unimos con Q
        dev_models = dev_models.filter(
            models.Q(device_model__office_id=office_id) |
            models.Q(switch_model__office_id=office_id)
        ).distinct()

    dev_models = dev_models.distinct()

    data = [{'id': m.id, 'name': m.dev_model} for m in dev_models]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_wall_port(request):

    wall_ports = Wall_Port.objects.all()

    wall_port_in_id = request.POST.get('wall_port_in_id') or request.GET.get('wall_port_in_id')

    location_id = request.POST.get('location_id') or request.GET.get('location_id')
    edifice_id = request.POST.get('edifice_id') or request.GET.get('edifice_id')
    office_id = request.POST.get('office_id') or request.GET.get('office_id')

    if location_id:
        wall_ports = wall_ports.filter(office__loc__edifice__location_id=location_id)
    if edifice_id:
        wall_ports = wall_ports.filter(office__loc__edifice_id=edifice_id)
    if office_id:
        wall_ports = wall_ports.filter(office_id=office_id)


    switch_wall_ports = Switch.objects.filter(wall_port_in__isnull=False).values_list('wall_port_in_id', flat=True)
    device_wall_ports = Device.objects.filter(wall_port_in__isnull=False).values_list('wall_port_in_id', flat=True)
    used_wall_ports = set(switch_wall_ports) | set(device_wall_ports)

    if not wall_port_in_id:
        wall_ports = wall_ports.exclude(id__in=used_wall_ports).order_by('wall_port')
    else:
        wall_ports = wall_ports.filter(id=wall_port_in_id).exclude(id__in=used_wall_ports).order_by('wall_port')

    print("Filtered WallPorts:", list(wall_ports.values_list('id', flat=True)))

    data = [
        {
            'id': w.id,
            'name': f'BOCA DE PARED: {w.wall_port} / OFICINA: {w.office} / EDIFICIO: {w.office.loc.edifice}'
        }
        for w in wall_ports
    ]
    return JsonResponse(data, safe=False)



@csrf_protect
@require_http_methods(["GET", "POST"])
def ajax_load_switch_port(request):

    switch_ports = Switch_Port.objects.all()

    switch_id = request.POST.get('switch_id') or request.GET.get('switch_id')

    exclude_switch_id = request.POST.get('exclude_switch_id') or request.GET.get('exclude_switch_id')

    switch_switch_ports = Switch.objects.filter(switch_port_in__isnull=False).values_list('switch_port_in_id', flat=True)
    device_switch_ports = Device.objects.filter(switch_port_in__isnull=False).values_list('switch_port_in_id', flat=True)
    used_switch_ports = set(switch_switch_ports) | set(device_switch_ports)

    if switch_id:
        switch_ports = switch_ports.filter(switch_id=switch_id)

    switch_ports = switch_ports.exclude(id__in=used_switch_ports).order_by('port_id')

    if exclude_switch_id:
        switch_ports = switch_ports.exclude(switch_id=exclude_switch_id)

    data = [{'id': sp.id, 'name': f'Puerto: {sp.port_id}'} for sp in switch_ports]
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_employee(request):
    province_id = request.POST.get('province_id') or request.GET.get('province_id')
    location_id = request.POST.get('location_id') or request.GET.get('location_id')
    dependency_id = request.POST.get('dependency_id') or request.GET.get('dependency_id')
    edifice_id = request.POST.get('edifice_id') or request.GET.get('edifice_id')
    loc_id = request.POST.get('loc_id') or request.GET.get('loc_id')
    office_id = request.POST.get('office_id')

    filters = {}
    if province_id:
        filters['office__loc__edifice__location__province_id'] = province_id
    if location_id:
        filters['office__loc__edifice__location_id'] = location_id
    if edifice_id:
        filters['office__loc__edifice_id'] = edifice_id
    if dependency_id:
        filters['office__dependency_id'] = dependency_id
    if loc_id:
        filters['office__loc_id'] = loc_id
    if office_id:
        filters['office_id'] = office_id

    employees = Employee.objects.filter(**filters).distinct()
    data = [
        {
            'id': e.id,
            'name': f'{e.employee_last_name}, {e.employee_name} - CUIL N°: {e.cuil} / Usuario: {e.user_pc}'
        }
        for e in employees
    ]
    return JsonResponse(data, safe=False)


@csrf_protect
@require_POST
def ajax_load_dev_type(request):
    usage = request.POST.get('usage', '')
    office_id = request.POST.get('office_id')

    dev_types = Dev_Type.objects.all()

    # Filtrar por usage
    if usage == 'device':
        dev_types = dev_types.exclude(dev_type='SWITCH')
    elif usage == 'switch':
        dev_types = dev_types.filter(dev_type='SWITCH')

    # Filtrar por office si corresponde (usando los nombres de relación correctos)
    if office_id:
        dev_types = dev_types.filter(
            Q(device_model__office_id=office_id) |
            Q(switch_model__office_id=office_id)
        ).distinct()

    data = []
    for dt in dev_types:
        data.append({
            'id': dt.id,
            'name': dt.dev_type,
            'dev_str': dt.dev_type
        })
    return JsonResponse(data, safe=False)

@csrf_protect
@require_POST
def ajax_load_province_location(request):
    office_id = request.POST.get('office_id')
    if not office_id:
        return JsonResponse({'error': 'No office_id provided'}, status=400)

    try:
        office = Office.objects.select_related('loc__edifice__location').get(id=office_id)
        location = office.loc.edifice.location
        province = location.province

        return JsonResponse({
            'province_id': province.id,
            'province_name': province.province,
            'location_id': location.id,
            'location_name': location.location,
        })
    except Office.DoesNotExist:
        return JsonResponse({'error': 'Office not found'}, status=404)


