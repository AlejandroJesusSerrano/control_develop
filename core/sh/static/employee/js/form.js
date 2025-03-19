$(document).ready(function() {
    $('.select2').select2({
        theme: 'bootstrap',
    });

    $('#custom_avatar_button').on('click', function() {
        $('#id_avatar_image_input').click();
    });

    $('#id_avatar_image_input').on('change', function() {
        const fileName = $(this).val().split('//').pop();
        $('#avatar_name').text(fileName || 'Ningún archivo seleccionado');
    });

    $('#toggle-office-filters').on('click', function (e) {
        e.preventDefault();
        const filterLocCards = $('#filter-office-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros de Localidades <i class="fas fa-search"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });

    $('#office_popup_add').on('click', function() {
        let url = officeAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Oficina', 'width=800,height=750');
        popup.focus();
    });

    $('#employee_status_popup_add').on('click', function() {
        let url = employee_statusAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Estado de Empleado', 'width=800,height=250');
        popup.focus();
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'officeAdded') {
            let officeId = event.data.id;
            let officeName = event.data.name;
            let select = $('#id_office');
            let option = new Option(officeName, officeId, true, true);
            select.append(option).val(officeId).trigger('change');
        }

        if (event.data.type === 'employee_statusAdded') {
            let statusId = event.data.id;
            let statusName = event.data.name;
            let select = $('#id_employee_status');
            let option = new Option(statusName, statusId, true, true);
            select.append(option).val(statusId).trigger('change');
        }
    });

    initializeFormSubmission('#myform', 'edit');

});

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        submit_with_ajax($(this).attr('action'), formData, function() {
        console.log('Formulario enviado y procesado con éxito');
        window.location.href = '/sh/employee/list';
        }, actionType);
    });
}