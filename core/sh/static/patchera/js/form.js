$(document).ready(function() {
    $('.select2').select2({
        theme:'bootstrap',
    });

    $('#toggle-rack-filters').on('click', function (e) {
        e.preventDefault();
        const filterLocCards = $('#filter-rack-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros <i class="fas fa-filter"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });

    $('#rack_popup_add').on('click', function (){
        let url = rackAddUrl + "?popup=1";
        let popup = window.open(url, 'rack_add_popup', 'width=800,height=600');
        popup.focus();
    })

    window.addEventListener('message', function(event) {
        if (event.data.type === 'rackAdded') {
            let rackId = event.data.id;
            let rackName = event.data.name;
            let select = $('#id_rack');
            let option = new Option(rackName, rackId, true, true);
            select.append(option).trigger('change');
            select.select2({theme: 'bootstrap'});
        }
    });

    if ('{{action}}' === 'edit') {
        let rackId = $('#id_rack').val();
        let rackName = $('#id_rack option:selected').text();

        if (rackId) {
            let newOption = new Option(rackName, rackId, true, true);
            $('#id_rack').append(newOption).trigger('change');
        }
    }

    initializeFormSubmission('#myForm', 'edit');

})

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();

        let formData = new FormData(this);

        submit_with_ajax($(this).attr('action'), formData, function() {
            console.log('Formulario enviado y procesado con éxito');
            window.location.href = '/sh/patchera/list';
        }, actionType)
    });
}