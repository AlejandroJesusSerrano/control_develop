from django.http import JsonResponse
from core.sh.forms.modals.forms import ProvinceModalForm


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

