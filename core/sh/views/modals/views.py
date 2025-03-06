from django.http import JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from core.sh.forms.modals.forms import DependencyModalForm, EdificeModalForm, LocationModalForm, OfficeLocModalForm, ProvinceModalForm


@require_http_methods(["GET", "POST"])  # Permite GET y POST
def province_modal_create(request):
    if request.method == 'POST':
        form = ProvinceModalForm(request.POST)
        if form.is_valid():
            province = form.save()
            # Devolver el fragmento de JavaScript para actualizar la ventana principal
            return HttpResponse(f'''
                <script type="text/javascript">
                    window.opener.postMessage({{
                        type: 'newObjectAdded',
                        selectId: 'id_province',
                        objectId: '{province.pk}',
                        objectName: '{province.province}'
                    }}, '*');
                    window.close();
                </script>
            ''')
        else:
            # Re-renderizar el formulario CON ERRORES
            return render(request, 'province/partials/province_form_modal_content.html', {'form': form})

    else:  # request.method == 'GET'
        form = ProvinceModalForm()  # Formulario vacío
        return render(request, 'province/partials/province_form_modal_content.html', {'form': form})


# def province_modal_create(request):
#     if request.method == 'POST':
#         form = ProvinceModalForm(request.POST)
#         if form.is_valid():
#             province = form.save()
#             return JsonResponse({
#                 'province_id': province.id,
#                 'province_name': province.province
#             })
#         else:
#             return JsonResponse({'error': form.errors}, status=400)
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)

@require_http_methods(["GET", "POST"])  # Permite GET y POST
def location_modal_create(request):
    if request.method == 'POST':
        form = LocationModalForm(request.POST)
        if form.is_valid():
            location = form.save()
            return HttpResponse(f'''
                <script type="text/javascript">
                    window.opener.postMessage({{
                        type: 'newObjectAdded',
                        selectId: 'id_location',
                        objectId: '{location.pk}',
                        objectName: '{location.location}'
                    }}, '*');
                    window.close();
                </script>
            ''')
        else:
            # Re-renderizar el formulario CON ERRORES
            return render(request, 'location/partials/location_form_modal_content.html', {'form': form})

    else:  # request.method == 'GET'
        form = ProvinceModalForm()  # Formulario vacío
        return render(request, 'location/partials/location_form_modal_content.html', {'form': form})

# def location_modal_create(request):
#     if request.method == 'POST':
#         form = LocationModalForm(request.POST)
#         if form.is_valid():
#             location = form.save()
#             return JsonResponse({
#                 'location_id': location.id,
#                 'location_name': location.location
#             })
#         else:
#             return JsonResponse({'error': form.errors}, status=400)
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)

def dependency_modal_create(request):
    if request.method == 'POST':
        form = DependencyModalForm(request.POST)
        if form.is_valid():
            dependency = form.save()
            return JsonResponse({
                'dependency_id': dependency.id,
                'dependency_name': dependency.dependency
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
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def office_loc_modal_create(request):
    if request.method == 'POST':
        form = OfficeLocModalForm(request.POST)
        if form.is_valid():
            office_loc = form.save()
            return JsonResponse({
                'office_loc_id': office_loc.id,
                'office_loc_name': office_loc.office_loc
            })
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


