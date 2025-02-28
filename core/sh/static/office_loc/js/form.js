$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
    });

    $('#id_province').select2({
        theme: 'bootstrap'
    });


    $('#id_location').select2({
        theme: 'bootstrap'
    });


    $('#province_add').on('click', function(e) {
        e.preventDefault();
        $('#provinceModal').modal('show');
    });

    $('#location_add').on('click', function(e) {
        e.preventDefault();
        $('#locationModal').modal('show');
    });

    // $('#locationModal').on('shown.bs.modal', function() {
    //     $('.select2').select2({
    //         theme: 'bootstrap'
    //     });
    // });

    $('#edifice_add').on('click', function(e) {
        e.preventDefault();
        $('#edificeModal').modal('show');
    });

    // enviar formulario de edificio (AJAX)
    $('#edificeForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
            $('#edificeModal').modal('hide');

            let newOption = new Option(response.edifice_name, response.edifice_id, true, true);
            $('#id_edifice').append(newOption).trigger('change')

            form.reset();
        }, 'add');
    });

    // enviar formulario de localidad (AJAX)
    $('#locationForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
            $('#locationModal').modal('hide');

            let newOption = new Option(response.location_name, response.location_id, true, true);
            $('#id_location').append(newOption).trigger('change');

            form.reset();
        }, 'add');
    });

    // enviar formulario de provincia (AJAX)
    $('#provinceForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

            $('#provinceModal').modal('hide');

            let newOption = new Option(response.province_name, response.province_id, true, true);
            $('#province_id').append(newOption).trigger('change');

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
