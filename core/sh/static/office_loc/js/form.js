$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
    });

    $('#toggle-edifice-filters').on('click', function(e) {
        e.preventDefault();
        const filterLocCards = $('#filter-edifice-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros <i class="fa fa-filter"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });

    $('#edifice_modal_add').on('click', function(e) {
        e.preventDefault();
        $('#edificeModal').modal('show');
    });

    // enviar formulario de edificio (AJAX)
    $('#edificeModalForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
            $('#edificeModal').modal('hide');

            let newOption = new Option(response.edifice_name, response.edifice_id, true, true);
            $('#id_edifice').append(newOption).trigger('change')

            form.reset();
        }, 'add');
    });

    $('#location_add_from_edifice_modal').on('click', function(e) {
        e.preventDefault();
        $('#locationModal').modal('show');
    });

    // enviar formulario de localidad (AJAX)
    $('#locationModalForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
            $('#locationModal').modal('hide');

            let newOption = new Option(response.location_name, response.location_id, true, true);
            $('#edificeModal').find('#id_modal_edifice_location_select').append(newOption).trigger('change')

            form.reset();
        }, 'add');
    });

    $('#province_add_from_location_modal').on('click', function(e) {
        e.preventDefault();
        $('#provinceModal').modal('show');
    });

    // enviar formulario de provincia (AJAX)
    $('#provinceModalForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

            $('#provinceModal').modal('hide');

            let newOption = new Option(response.province_name, response.province_id, true, true);
            $('#locationModal').find('#id_modal_location_province_select').append(newOption).trigger('change')

            form.reset();
        }, 'add');
    });

    if ('{{action}}' === 'edit') {
        let edificeId = $('#id_edifice').val();
        let edificeName = $('#id_edifice option:selected').text();

        if (edificeId) {
            let newOption = new Option(edificeName, edificeId, true, true);
            $('#id_edifice').append(newOption).trigger('change');
        }
    }


    initializeFormSubmission('#myform', 'edit')

});

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();

        let formData = new FormData(this);

        submit_with_ajax($(this).attr('action'), formData, function() {
            console.log('Formulario enviado y procesado con éxito');
            window.location.href = '/sh/office_loc/list';
        }, actionType)
    });
}
