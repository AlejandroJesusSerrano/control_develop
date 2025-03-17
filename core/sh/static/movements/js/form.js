$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  $('#id_movements_date_in_button').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true,
    language: 'es',
    container: 'body',
    orientation: 'auto',
    zIndexOffset: 1050
  }).on('changeDate', function(e) {
    $('#id_movements_date_in_input').val(e.format('dd/mm/yyyy'));
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
      ? 'Filtros <i class="fa fa-filter"></i>'
      : 'Ocultar Filtros <i class="fas fa-times"></i>');
  });

  $('#office_popup_add').on('click', function() {
    let url = officeAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Oficina', 'width=800,height=800');
    popup.focus();
  });

  $('#employee_popup_add').on('click', function() {
    let url = employeeAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Empleado', 'width=800,height=700');
    popup.focus();
  });

  $('#device_popup_add').on('click', function() {
    let url = deviceAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Dispositivo', 'width=800,height=1080');
    popup.focus();
  });

  $('#switch_popup_add').on('click', function() {
    let url = switchAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Switch', 'width=800,height=800');
    popup.focus();
  });

  $('#move_type_popup_add').on('click', function() {
    let url = moveTypeAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Tipo de Movimiento', 'width=800,height=350');
    popup.focus();
  });

  window.addEventListener('message', function(event) {
    if (event.data.type === 'officeAdded') {
      let office_id = event.data.id;
      let office_name = event.data.name;
      let select = $('#id_office');
      let option = new Option(office_name, office_id, true, true);
      select.append(option).val(officeId).trigger('change');
    }

    if (event.data.type === 'employeeAdded') {
      let employee_id = event.data.id;
      let employee_name = event.data.name;
      let select = $('#id_employee');
      let option = new Option(employee_name, employee_id, true, true);
      select.append(option).val(employeeId).trigger('change');
    }

    if (event.data.type === 'deviceAdded') {
      let device_id = event.data.id;
      let device_name = event.data.name;
      let select = $('#id_device');
      let option = new Option(device_name, device_id, true, true);
      select.append(option).val(deviceId).trigger('change');
    }

    if (event.data.type === 'switchAdded') {
      let switch_id = event.data.id;
      let switch_name = event.data.name;
      let select = $('#id_switch');
      let option = new Option(switch_name, switch_id, true, true);
      select.append(option).val(switchId).trigger('change');
    }

    if (event.data.type === 'moveTypeAdded') {
      let move_type_id = event.data.id;
      let move_type_name = event.data.name;
      let select = $('#id_movements_type');
      let option = new Option(move_type_name, move_type_id, true, true);
      select.append(option).val(moveTypeId).trigger('change');
    }
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
