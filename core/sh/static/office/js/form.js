$(document).ready(function() {

    $('.select2').select2({
        theme:'bootstrap',
    });


    $('#toggle-office-filters').on('click', function(e) {
        e.preventDefault();
        const filterLocCards = $('#filter-office-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros <i class="fa fa-filter"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });

    $('#dependency_popup_add').on('click', function() {
        let url = dependencyAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Dependencia', 'width=800,height=600');
        popup.focus();
    });

    $('#edifice_popup_add').on('click', function() {
        let url = edificeAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Edificio', 'width=800,height=600');
        popup.focus();
    });

    $('#office_loc_popup_add').on('click', function() {
        let url = officeLocAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Ubicación de Oficina', 'width=800,height=600');
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

        if (event.data.type === 'dependencyAdded') {
            let dependencyId = event.data.id;
            let dependencyName = event.data.name;
            let select = $('#id_dependency');
            let option = new Option(dependencyName, dependencyId, true, true);
            select.append(option).val(dependencyId).trigger('change');
        }

        if (event.data.type === 'office_locAdded') {
            let locId = event.data.id;
            let locName = event.data.name;
            let select = $('#id_loc');
            let option = new Option(locName, locId, true, true);
            select.append(option).val(locId).trigger('change');
        };
    });


    if ('{{action}}' === 'edit') {
        let edificeId = $('#id_edifice').val();
        let edificeName = $('#id_edifice option:selected').text();
        let depdendecyId = $('#id_dependency').val();
        let depdendecyName = $('#id_dependency option:selected').text();
        let locId = $('#id_loc').val();
        let locName = $('#id_loc option:selected').text();

        if (edificeId) {
            let newOption = new Option(edificeName, edificeId, true, true);
            $('#id_edifice').append(newOption).trigger('change');
        }

        if (depdendecyId) {
            let newOption = new Option(depdendecyName, depdendecyId, true, true);
            $('#id_dependency').append(newOption).trigger('change');
        }

        if (locId) {
            let newOption = new Option(locName, locId, true, true);
            $('#id_loc').append(newOption).trigger('change');
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
            window.location.href = '/sh/office/list/';
        }, actionType);
    });
}

