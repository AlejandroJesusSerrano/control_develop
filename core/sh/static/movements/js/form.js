$(document).ready(function() {
  // Inicializar todos los selects con select2
  $('.select2').select2({ theme: 'bootstrap' });

  // ---------- INICIALIZAR DATEPICKER ----------
  $('#id_suply_date_in_input').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true,
    language: 'es',
    orientation: 'auto',
    zIndexOffset: 1050
  }).on('changeDate', function(e) {
    $('#id_suply_date_in_input').val(e.format('dd/mm/yyyy'));
  });

  $('#id_suply_date_in_button').on('click', function() {
    $('#id_suply_date_in_input').datepicker('show');
  });

  if ($('#id_office').length > 0) {
    $('select[name="office"]').on('change', function() {
      const office_id = $(this).val();
      updateDeviceOffices(office_id);
      updateSwitchOffices(office_id);
      updateEmployeeOffices(office_id);
    });
  }

  $('#toggle-office-filters').on('click', function(e) {
    e.preventDefault();
    let filterOfficeCards = $('#filter-office-cards');
    filterOfficeCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    $(this).html(filterOfficeCards.hasClass('d-none')
      ? 'Filtrar Oficinas y Empleados <i class="fa fa-filter"></i>'
      : 'Ocultar Filtros <i class="fas fa-times"></i>');
  });

  initializeFormSubmission('#myform', 'edit');

});

function updateEmployeeOffices(office_id) {
  updateOptions('/sh/ajax/load_employee/', {
    office_id: office_id,
  }, $('select[name="employee"]'), $('#id_employee').data('preselected'));
}

function updateDeviceOffices(office_id) {
  updateOptions('/sh/ajax/load_device/', {
    office_id: office_id,
  }, $('select[name="device"]'), $('#id_device').data('preselected'));
}

function updateSwitchOffices(office_id) {
  updateOptions('/sh/ajax/load_switch/', {
    office_id: office_id,
  }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
}


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
