from django.http import JsonResponse
from core.sh.forms.modals.forms import EdificeModalForm, LocationModalForm, ProvinceModalForm


def province_modal_create(request):
    if request.method == 'POST':
        form = ProvinceModalForm(request.POST)
        if form.is_valid():
            province = form.save()
            return JsonResponse({
                'province_id': province.id,
                'province_name': province.province
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def location_modal_create(request):
    if request.method == 'POST':
        form = LocationModalForm(request.POST)
        if form.is_valid():
            location = form.save()
            return JsonResponse({
                'location_id': location.id,
                'location_name': location.location
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def edifice_modal_create(request):
    if request.method == 'POST':
        form = EdificeModalForm(request.POST)
        if form.is_valid():
            edifice = form.save()
            return JsonResponse({
                'edifice_id': edifice.id,
                'edifice_name': edifice.edifice
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)

