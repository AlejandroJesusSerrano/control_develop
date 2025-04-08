$(document).ready(function() {

    $('.select2').select2({
        theme:'bootstrap'
    });

    $('#id_send_date_button').datepicker({
        format: 'dd/mm/yyyy',
        autoclose: true,
        todayHighlight: true,
        language: 'es',
        container: 'body',
        orientation: 'auto',
        zIndexOffset: 1050
    }).on('changeDate', function(e) {
        var selectedDate = e.format('dd/mm/yyyy');
        $('#id_send_date_display').val(selectedDate);
        $('#id_send_date').val(selectedDate);
    });

    // Datepicker para reception_date
    $('#id_reception_date_button').datepicker({
        format: 'dd/mm/yyyy',
        autoclose: true,
        todayHighlight: true,
        language: 'es',
        container: 'body',
        orientation: 'auto',
        zIndexOffset: 1050
    }).on('changeDate', function(e) {
        var selectedDate = e.format('dd/mm/yyyy');
        $('#id_reception_date_display').val(selectedDate);
        $('#id_reception_date').val(selectedDate);
    });

    initializeFormSubmission('#myform', 'edit')

});

$('#switch_popup_add').on('click', function() {
let url = switchAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Switch', 'width=800,height=825');
    popup.focus();
});

window.addEventListener('message', function(event) {
    if (event.data.type === 'switchAdded') {
        let switchId = event.data.id;
        let switchName = event.data.name;
        let select = $('#id_switch');
        let option = new Option(switchName, switchId, true, true);
        select.append(option).val(switchId).trigger('change');
    }
});

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        submit_with_ajax($(this).attr('action'), formData, function() {
            console.log('Formulario enviado y procesado con éxito');
            window.location.href = '/sh/switch/list';
        }, actionType);
    });
}

