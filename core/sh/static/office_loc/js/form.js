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

    $('#edifice_add_popup').on('click', function() {
        let url = edificeAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Edificio', 'width=800,height=600');
        popup.focus();
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'edificeAdded') {
            let edificeId = event.data.id;
            let edificeName = event.data.name;
            let select = $('#id_edifice');
            let option = new Option(edificeName, edificeId, true, true);
            select.append(option).val(edificeId).trigger('change');
        }
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
