from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect

from core.sh.models.dependency.models import Dependency
from core.sh.models.dev_model.models import Dev_Model
from core.sh.models.edifice.models import Edifice
from core.sh.models.employee.models import Employee
from core.sh.models.location.models import Location
from core.sh.models.office.models import Office
from core.sh.models.office_loc.models import Office_Loc
from core.sh.models.switch_port.models import Switch_Port
from core.sh.models.wall_port.models import Wall_Port

@csrf_protect
def ajax_load_location(request):
  data=[]
  if request.method == 'POST':
    province_id = request.POST.get('province_id')
    locations = Location.objects.filter(province_id=province_id)
    data = [{'id': l.id, 'name': l.location} for l in locations]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_dependency(request):
  data = []
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    dependencies = Dependency.objects.filter(edifice__location_id=location_id)
    data = [{'id': d.id, 'name': d.dependency} for d in dependencies]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_edifices(request):
  data = []
  if request.method == 'POST':
    location_id = request.POST.get('location_id')
    edifices = Edifice.objects.filter(location_id=location_id)
    data = [{'id': e.id, 'name': e.edifice} for e in edifices]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_loc(request):
  data = []
  if request.method == 'POST':
    edifice_id = request.POST.get('edifice_id')
    locs = Office_Loc.objects.filter(edifice_id=edifice_id)
    data = [{'id': loc.id, 'name': f'Piso: {loc.floor} / Ala: {loc.wing}'} for loc in locs]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_office(request):
  data = []
  if request.method == 'POST':
    loc_id = request.POST.get('loc_id')
    offices = Office.objects.filter(loc_id=loc_id)
    data = [{'id': o.id, 'name': o.office} for o in offices]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_wall_port(request):
  data = []
  if request.method == 'POST':
    office_id = request.POST.get('office_id')
    wall_ports = Wall_Port.objects.filter(office_id=office_id)
    data = [{'id': w.id, 'name': w.wall_port} for w in wall_ports]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_switch_port(request):
  data = []
  if request.method == 'POST':
    office_id = request.POST.get('office_id')
    switch_ports = Switch_Port.objects.filter(switch__office_id=office_id)
    data = [{'id': s.id, 'name': f'Puerto: {s.port_id}, Switch: {s.switch}'} for s in switch_ports]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_employee(request):
  data = []
  if request.method == 'POST':
    office_id = request.POST.get('office_id')
    employees = Employee.objects.filter(office_id=office_id)
    data = [{'id': e.id, 'name': f'{e.employee_last_name}, {e.employee_name}'} for e in employees]
  return JsonResponse(data, safe=False)

@csrf_protect
def ajax_load_model(request):
  data = []
  if request.method == 'POST':
    brand_id = request.POST.get('brand_id')
    dev_type_id = request.POST.get('dev_type_id')
    models = Dev_Model.objects.filter(brand_id=brand_id, dev_type_id=dev_type_id)
    data = [{'id': m.id, 'name': m.dev_model} for m in models]
  return JsonResponse(data, safe=False)