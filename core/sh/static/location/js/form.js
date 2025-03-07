// SELECT 2

$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
    });

    $('#province_add_popup').on('click', function() {
        let url = provinceAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Provincia', 'width=800,height=300');
        popup.focus();
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'provinceAdded') {
            let provinceId = event.data.id;
            let provinceName = event.data.name;
            let select = $('#id_province');
            let option = new Option(provinceName, provinceId, true, true);
            select.append(option).trigger('change');
            select.select2({ theme: 'bootstrap' });
        }
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
