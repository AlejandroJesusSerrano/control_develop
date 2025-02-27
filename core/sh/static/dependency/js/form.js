$(document).ready(function() {

$('.select2').select2({
    theme: 'bootstrap',
});

// Abrir modal de localidad
$('#location_add').on('click', function(e) {
    e.preventDefault();
    $('#locationModal').modal('show');
});

// Abrir modal de provincia desde el modal de localidad
$('#locationModal').on('click', '#province_add_from_location', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
});


// Enviar formulario de localidad (AJAX)
$('#locationForm').on('submit', function(e) {
    e.preventDefault();
    var form = this;
    submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {

        $('#locationModal').modal('hide');

        var newOption = new Option(response.location_name, response.location_id, true, true);
        $('#id_location').append(newOption).trigger('change');

        form.reset();
    },'add');

});

// Enviar formulario de provincia (AJAX)
$('#provinceForm').on('submit', function(e) {
    e.preventDefault();
    var form = this;
    submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {

        $('#provinceModal').modal('hide');

        var newOption = new Option(response.province_name, response.province_id, true, true);
        $('#locationModal').find('#id_province').append(newOption).trigger('change');

        form.reset();
    }, 'add');
});

if ('{{action}}' === 'edit') {
    var locationId = $('#id_location').val();
    var locationName = $('#id_location option:selected').text();

    if (locationId) {
        var newOption = new Option(locationName, locationId, true, true);
        $('#id_location').append(newOption).trigger('change');
    }
}


initializeFormSubmission('#dependencyForm', 'edit');
});

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();

        let formData = new FormData(this);

        submit_with_ajax($(this).attr('action'), formData, function() {
            console.log('Formulario enviado y procesado con éxito');
            window.location.href = '/sh/dependency/list'; // Redirige, pero idealmente usa AJAX también
        }, actionType)
    });
}