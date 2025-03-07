$(document).ready(function() {

    $('.select2').select2({
        theme: 'bootstrap',
    });

    $('#location_add_popup').on('click', function() {
        let url = locationAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Localidad', 'width=800,height=380');
        popup.focus();
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'locationAdded') {
            let locationId = event.data.id;
            let locationName = event.data.name;
            let select = $('#id_location');
            let option = new Option(locationName, locationId, true, true);
            select.append(option).val(locationId).trigger('change');
        }
    });


    if ('{{action}}' === 'edit') {
        let locationId = $('#id_location').val();
        let locationName = $('#id_location option:selected').text();

        if (locationId) {
            let newOption = new Option(locationName, locationId, true, true);
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
            window.location.href = '/sh/dependency/list';
        }, actionType)
    });
}