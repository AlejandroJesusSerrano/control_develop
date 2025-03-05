// SELECT 2

$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
    });

    $('#province_modal_add').on('click', function(e) {
        e.preventDefault();
        $('#provinceModal').modal('show');
    });

    $('#provinceForm').on('submit', function(e) {
        e.preventDefault();
        let form = this;
        submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {

            $('#provinceModal').modal('hide');

            let newOption = new Option(response.province_name, response.province_id, true, true);
            $('#id_province').append(newOption).trigger('change');

        form.reset();
    },'add');

});

if ('{{action}}' === 'edit') {
    let provinceId = $('#id_province').val();
    let provinceName = $('#id_province option:selected').text();

    if (provinceId) {
        let newOption = new Option(provinceName, provinceId, true, true);
        $('#id_province').append(newOption).trigger('change');
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
            window.location.href = '/sh/location/list';
        }, actionType)
    });
}
