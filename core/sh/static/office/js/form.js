$(document).ready(function() {

    $('.select2').select2({
        theme:'bootstrap',
    });

    function openPopup(url) {
        const width = 800;
        const height = 300;
        const left = (window.innerWidth - width) / 2;
        const top = (window.innerHeight - height) / 2;
        const options = `width=${width},height=${height},top=${top},left=${left},resizable=yes,scrollbars=yes`;

        window.open(url, '_blank', options);
    }

    // --- Manejador para los enlaces 'add-related' ---
    $(document).on('click', '.add-related', function(e) {
        e.preventDefault();  // Evita el comportamiento predeterminado del enlace
        const popupUrl = $(this).data('popup-url'); // Obtiene la URL del atributo data-popup-url
        openPopup(popupUrl); // Abre la ventana emergente
    });

     // --- Función para recibir mensajes del popup ---
    window.addEventListener('message', function(event) {
        if (event.data.type === 'newObjectAdded') {
            const selectId = event.data.selectId;
            const objectId = event.data.objectId;
            const objectName = event.data.objectName;

            // Crear la nueva opción
            const newOption = new Option(objectName, objectId, true, true);

            // Añadir y seleccionar la opción en el select correspondiente
            $('#' + selectId).append(newOption).val(objectId).trigger('change');
        }
    });

    $('#toggle-office-filters').on('click', function(e) {
        e.preventDefault();
        const filterLocCards = $('#filter-office-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros <i class="fa fa-filter"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });

    if ($('#id_location').length > 0) {
        $('select[name="location"]').on('change', async function() {
            const location_id = $(this).val();
            if (!location_id) {
                console.warn('No se ha seleccionado una localidad válida en el formulario de Oficina.');
                clearDependentFields(['#id_edifice', '#id_loc', '#id_dependency']);
                return;
            }
            console.log('Localidad seleccionada con ID:', location_id);
            await updateOptions('/sh/ajax/load_office/', { 'location_id': location_id }, $('#id_edifice'));
        });
    }

//     // Abrir modal de dependencia
//     $('#dependency_add_modal').on('click', function(e) {
//         e.preventDefault();
//         $('#dependencyModal').modal('show');
//     });

//     $('#dependencyModalForm').on('submit', function(e) {
//         e.preventDefault();
//         let form = this;
//         submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
//             console.log('Respuesta AJAX: ', response);
//             $('#dependencyModal').modal('hide');

//             let newOption = new Option(response.dependency_name, response.dependency_id, true, true);
//             $('#id_dependency').append(newOption).trigger('change')

//             form.reset();
//         }, 'add');
//     });


//     // Abrir modal de edificio
//     $('#edifice_add_modal').on('click', function(e) {
//         e.preventDefault();
//         $('#edificeModal').modal('show');
//     });

//     $('#edificeModalForm').on('submit', function(e) {
//         e.preventDefault();
//         let form = this;
//         submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
//             console.log('Respuesta AJAX: ', response);
//             $('#edificeModal').modal('hide');

//             let newOption = new Option(response.edifice_name, response.edifice_id, true, true);
//             $('#id_edifice').append(newOption).trigger('change')

//             form.reset();
//         }, 'add');
//     });

//     $('#location_add_from_edifice_modal').on('click', function(e) {
//         e.preventDefault();
//         $('#locationModal').modal('show');
//     });

//     $('#location_add_from_dependency_modal').on('click', function(e) {
//         e.preventDefault();
//         $('#locationModal').modal('show');
//     });

//     $('#locationModalForm').on('submit', function(e) {
//         e.preventDefault();
//         let form = this;
//         submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

//             $('#locationModal').modal('hide');

//             let newOption = new Option(response.location_name, response.location_id, true, true);

//             // Actualiza ambos campos de selección
//             $('#edificeModal').find('#id_modal_edifice_location_select').append(newOption).trigger('change');
//             $('#dependencyModal').find('#id_modal_dependency_location_select').append(newOption).trigger('change');

//             form.reset();
//         }, 'add');
//     });

//     // Abrir modal de provincia desde modal de localidad
//     $('#province_add_from_location_modal').on('click', function(e) {
//         e.preventDefault();
//         $('#provinceModal').modal('show');
//     });

//     $('#provinceModalForm').on('submit', function(e) {
//         e.preventDefault();
//         let form = this;
//         submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

//             $('#provinceModal').modal('hide');

//             let newOption = new Option(response.province_name, response.province_id, true, true);
//             $('#locationModal').find('#id_modal_location_province_select').append(newOption).trigger('change')
//             $('#id_province').append(newOption).trigger('change')

//             form.reset();
//         }, 'add');
//     });


//     // Abrir modal de ubicación de oficina
//     $('#loc_add').on('click', function(e) {
//         e.preventDefault();
//         $('#locModal').modal('show')
//     });

//     $('#locModalForm').on('submit', function(e) {
//         e.preventDefault();
//         let form = this;
//         submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
//             console.log('Respuesta AJAX: ', response);
//             $('#locModal').modal('hide');

//             let newOption = new Option(response.loc_name, response.loc_id, true, true);
//             $('#id_loc').append(newOption).trigger('change')

//             form.reset();
//         }, 'add');
//     });

//     if ('{{action}}' === 'edit') {
//         let edificeId = $('#id_edifice').val();
//         let edificeName = $('#id_edifice option:selected').text();
//         let depdendecyId = $('#id_dependency').val();
//         let depdendecyName = $('#id_dependency option:selected').text();
//         let locId = $('#id_loc').val();
//         let locName = $('#id_loc option:selected').text();

//         if (edificeId) {
//             let newOption = new Option(edificeName, edificeId, true, true);
//             $('#id_edifice').append(newOption).trigger('change');
//         }

//         if (depdendecyId) {
//             let newOption = new Option(depdendecyName, depdendecyId, true, true);
//             $('#id_dependency').append(newOption).trigger('change');
//         }

//         if (locId) {
//             let newOption = new Option(locName, locId, true, true);
//             $('#id_loc').append(newOption).trigger('change');
//         }
//     }

//     initializeFormSubmission('#myform', 'edit');

// });

// function initializeFormSubmission(formSelector, actionType) {
//     $(formSelector).on('submit', function(e) {
//         e.preventDefault();

//         let formData = new FormData(this);

//         submit_with_ajax($(this).attr('action'), formData, function() {
//             console.log('Formulario enviado y procesado con éxito');
//             window.location.href = '/sh/wall_port/list/';
//         }, actionType);
//     });
// }

// let activeRequests = {}; // Objeto para almacenar peticiones activas

// async function updateOptions(url, data, $select) {
//     const selectId = $select.attr('id');

//     // Abortar peticiones anteriores para el mismo select
//     if (activeRequests[selectId]) {
//         activeRequests[selectId].abort();
//     }

//     try {
//         // Iniciar nueva petición y almacenarla
//         activeRequests[selectId] = $.ajax({
//             url: url,
//             data: data
//         });

//         const response = await activeRequests[selectId]; // Esperar la petición actual

//         let options = '<option value="">---------</option>';
//         for (const [key, value] of Object.entries(response)) {
//             options += `<option value="${key}">${value}</option>`;
//         }
//         $select.html(options);
//     } catch (error) {
//         if (error.statusText !== 'abort') { // Ignorar errores de aborto intencional
//             console.error('Error al cargar opciones:', error);
//         }
//     } finally {
//         delete activeRequests[selectId]; // Limpiar petición al finalizar
//     }
// }

