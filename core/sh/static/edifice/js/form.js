$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
    });


$('#location_modal_add').on('click', function(e) {
    e.preventDefault();
    $('#locationModal').modal('show');
});


$('#locationModal').on('click', '#province_add_from_location', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
});


// Enviar formulario de localidad (AJAX)
$('#locationModalForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {

        $('#locationModal').modal('hide');

        let newOption = new Option(response.location_name, response.location_id, true, true);
        $('#id_location').append(newOption).trigger('change');

        form.reset();
    },'add');

});

// Enviar formulario de provincia (AJAX)
$('#provinceModalForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {

        $('#provinceModal').modal('hide');

        let newOption = new Option(response.province_name, response.province_id, true, true);
        $('#locationModal').find('#id_modal_location_province_select').append(newOption).trigger('change');

        form.reset();
    }, 'add');
});

if ('{{action}}' === 'edit') {
    let locationId = $('#id_location').val();
    let locationName = $('#id_location option:selected').text();

    if (locationId) {
        let newOption = new Option(locationName, locationId, true, true);
        $('#id_location').append(newOption).trigger('change');
    }
}

initializeFormSubmission('#myform', 'edit');

});

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();

        let formData = new FormData(this);

        submit_with_ajax($(this).attr('action'), formData, function() {
            console.log('Formulario enviado y procesado con éxito');
            window.location.href = '/sh/edifice/list';
        }, actionType)
    });
}