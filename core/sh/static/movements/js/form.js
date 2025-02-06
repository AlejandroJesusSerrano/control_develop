$(document).ready(function() {
  $('.select2').select2({ theme: 'bootstrap' });

  // Inicializar datepicker sobre el input "oculto"
  $('#id_suply_date_in_input').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true,
    language: 'es',
    // Omitir container:'body' para que se posicione de forma relativa
    orientation: 'auto',
    zIndexOffset: 1050
  }).on('changeDate', function(e) {
    $('#id_suply_date_in_input').val(e.format('dd/mm/yyyy'));
  });

  $('#id_suply_date_in_button').on('click', function() {
    $('#id_suply_date_in_input').datepicker('show');
  });

  // Evento al cambiar la oficina
  $('select[name="office"]').on('change', function() {
    const office_id = $(this).val();
    if (office_id) {
        updateRackOptions(office_id);
        updateBrandOptions(null, office_id);
        updateSerialNumberOptions(null, null, office_id);
    }
  });

  // Evento al cambiar el tipo de dispositivo
  $('select[name="dev_type"]').on('change', function() {
    const dev_type = $(this).val();
    const office_id = $('select[name="office"]').val();

    updateBrandOptions(dev_type, office_id);
    updateSerialNumberOptions(dev_type, null, office_id);

    if (dev_type === "SWITCH") {
        $('select[name="device_serial_n"]').prop('disabled', true).val('').trigger('change');
        $('select[name="switch_serial_n"]').prop('disabled', false);
        $('select[name="rack"], select[name="switch_rack_pos"]').prop('disabled', false);
    } else {
        $('select[name="switch_serial_n"]').prop('disabled', true).val('').trigger('change');
        $('select[name="device_serial_n"]').prop('disabled', false);
        $('select[name="rack"], select[name="switch_rack_pos"]').prop('disabled', true).val('').trigger('change');
    }
  });

  // Evento al cambiar la marca
  $('select[name="brand"]').on('change', function() {
    const brand_id = $(this).val();
    const dev_type = $('select[name="dev_type"]').val();
    const office_id = $('select[name="office"]').val();
    updateSerialNumberOptions(dev_type, brand_id, office_id);
  });
  // // Evento para dev_type: actualizar campos según el tipo seleccionado
  // $('select[name="dev_type"]').on('change', function() {
  //   const dev_type_val = $(this).val();
  //   const dev_type_text = $('select[name="dev_type"] option:selected').text().trim().toUpperCase();
  //   const office_id = $('select[name="office"]').val() || null;

  //   if (dev_type_text === "SWITCH") {

  //     $('select[name="device"]').val('').trigger('change.select2').prop('disabled', true);

  //     $('select[name="switch"]').prop('disabled', false);

  //     updateBrandOptions(dev_type_val, 'switch', office_id);
  //     updateIpOptions(dev_type_val, 'switch', office_id);
  //     updateSwitchOptions(dev_type_val, null, office_id);
  //     updateSwitchSerialNOptions($('select[name="brand"]').val(), office_id);

  //     $('select[name="switch_serial_n"]').prop('disabled', false);
  //     $('select[name="switch_rack_pos"]').prop('disabled', false);
  //     $('select[name="rack"]').prop('disabled', false);
  //     $('select[name="device_serial_n"]').val('').trigger('change.select2').prop('disabled', true);

  //   } else {

  //     $('select[name="switch"]').val('').trigger('change.select2').prop('disabled', true);

  //     $('select[name="device"]').prop('disabled', false);
  //     updateBrandOptions(dev_type_val, 'device', office_id);
  //     updateIpOptions(dev_type_val, 'device', office_id);
  //     updateModelOptions(dev_type_val, null, office_id);
  //     updateDeviceSerialNOptions(dev_type_val, $('select[name="brand"]').val(), office_id);

  //     $('select[name="device_serial_n"]').prop('disabled', false);
  //     $('select[name="rack"]').val('').trigger('change.select2').prop('disabled', true);
  //     $('select[name="switch_serial_n"]').val('').trigger('change.select2').prop('disabled', true);
  //     $('select[name="switch_rack_pos"]').val('').trigger('change.select2').prop('disabled', true);
  //   }
  // });

  // $('select[name="brand"]').on('change', function() {
  //   const brand_id = $(this).val();
  //   const dev_type_val = $('select[name="dev_type"]').val();
  //   const office_id = $('select[name="office"]').val() || null;
  //   const dev_type_text = $('select[name="dev_type"] option:selected').text().trim().toUpperCase();
  //   if (dev_type_text === "SWITCH") {
  //     updateSwitchOptions(dev_type_val, brand_id, office_id);
  //     updateSwitchSerialNOptions(brand_id, office_id);
  //   } else {
  //     updateModelOptions(dev_type_val, brand_id, office_id);
  //     updateDeviceSerialNOptions(dev_type_val, brand_id, office_id);
  //   }
  // });

  if ($('#id_office').length > 0) {
    $('#id_office').off('change');
    $('#id_office').on('change', function() {
      const office_id = $(this).val();
      if (office_id) {
        $.ajax({
          url: '/sh/ajax/load_province_location/',
          type: 'POST',
          data: { 'office_id': office_id },
          dataType: 'json',
          success: function(data) {
            if (!data.error) {
              $('select[name="province"]').val(data.province_id).trigger('change.select2');
              $('select[name="location"]').val(data.location_id).trigger('change.select2').trigger('change');
              $('#id_office').val(office_id).trigger('change.select2').select2('destroy').select2({ theme: 'bootstrap' });
              if ($('#id_employee').length > 0) {
                updateOptions('/sh/ajax/load_employee/', { 'office_id': office_id }, $('select[name="employee"]'), $('#id_employee').data('preselected'));
              }
              // Con la oficina seleccionada, actualizar los modelos y demás filtros según el dev_type actual
              const dev_type_val = $('select[name="dev_type"]').val();
              const dev_type_text = $('select[name="dev_type"] option:selected').text().trim().toUpperCase();
              const brand_id = $('select[name="brand"]').val();
              if (dev_type_text === "SWITCH") {
                updateSwitchOptions(dev_type_val, brand_id, office_id);
                updateBrandOptions(dev_type_val, 'switch', office_id);
                updateIpOptions(dev_type_val, 'switch', office_id);
              } else {
                updateModelOptions(dev_type_val, brand_id, office_id);
                updateBrandOptions(dev_type_val, 'device', office_id);
                updateIpOptions(dev_type_val, 'device', office_id);
              }
            } else {
              console.error('Error: ', data.error);
            }
          },
          error: function(xhr, status, error) {
            console.error('AJAX Error: ', status, error);
          }
        });
      }
    });
  }


  // Toggle para filtros de dispositivos
  $('#toggle-device-filters').on('click', function(e) {
    e.preventDefault();
    const filterDeviceCards = $('#filter-device-cards');
    filterDeviceCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    if (filterDeviceCards.hasClass('d-none')) {
      $(this).html('Filtrar Dispositivos <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class="fas fa-times"></i>');
    }
  });

  // Toggle para filtros de oficinas y empleados
  $('#toggle-office-filters').on('click', function(e) {
    e.preventDefault();
    const filterOfficeCards = $('#filter-office-cards');
    filterOfficeCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    if (filterOfficeCards.hasClass('d-none')) {
      $(this).html('Filtrar Oficinas y Empleados <i class="fa fa-filter"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class="fas fa-times"></i>');
    }
  });

  // Actualizar empleado al cambiar la oficina
  if ($('#id_office').length > 0) {
    $('#id_office').off('change');
    $('#id_office').on('change', function() {
      const office_id = $(this).val();
      if (office_id) {
        $.ajax({
          url: '/sh/ajax/load_province_location/',
          type: 'POST',
          data: { 'office_id': office_id },
          dataType: 'json',
          success: function(data) {
            if (!data.error) {
              $('select[name="province"]').val(data.province_id).trigger('change.select2');
              $('select[name="location"]').val(data.location_id).trigger('change.select2').trigger('change');
              $('#id_office').val(office_id).trigger('change.select2').select2('destroy').select2({ theme: 'bootstrap' });
              if ($('#id_employee').length > 0) {
                updateOptions('/sh/ajax/load_employee/', { 'office_id': office_id }, $('select[name="employee"]'), $('#id_employee').data('preselected'));
              }
            } else {
              console.error('Error: ', data.error);
            }
          },
          error: function(xhr, status, error) {
            console.error('AJAX Error: ', status, error);
          }
        });
      }
    });
  }

  // Inicializar envío del formulario
  initializeFormSubmission('#myform', 'edit');  // Asumiendo que formId se define en el template
});


// Función para actualizar marcas filtradas
// function updateBrandOptions(dev_type_val, usage, office_id) {
//   updateOptions('/sh/ajax/load_brand/', {
//     'dev_type_name': dev_type_val,
//     'usage': usage,
//     'office_id': office_id
//   }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
// }

function updateBrandOptions(dev_type, office_id) {
  updateOptions('/sh/ajax/load_brand/', { 'dev_type_name': dev_type, 'office_id': office_id }, $('select[name="brand"]'));
}

// Función para actualizar los nuemros de serie de dispositivos filtrados
// function updateDeviceSerialNOptions(dev_type_val, brand_id, office_id) {
//   updateOptions('/sh/ajax/load_device_serial_n/', {
//     'dev_type_name': dev_type_val,
//     'brand_id': brand_id,
//     'office_id': office_id
//   }, $('select[name="device_serial_n"]'), $('#id_device_serial_n').data('preselected'));
// }

// Función para actualizar IPs filtradas
function updateIpOptions(dev_type_val, usage, office_id) {
  updateOptions('/sh/ajax/load_ip/', {
    'dev_type_name': dev_type_val,
    'usage': usage,
    'office_id': office_id
  }, $('select[name="ip"]'), $('#id_ip').data('preselected'));
}

// Función para actualizar modelos (dispositivos) filtrados
function updateModelOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'device',
    'office_id': office_id
  }, $('select[name="device"]'), $('#id_device').data('preselected'));
}

// Función para actualizar los Racks filtrados
// function updateRackOptions(office_id) {
//   updateOptions('/sh/ajax/load_rack/', {
//     'office_id': office_id
//   }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
// }
function updateRackOptions(office_id) {
  updateOptions('/sh/ajax/load_rack/', { 'office_id': office_id }, $('select[name="rack"]'));
}

// Función para actualizar Posiciones del Rack filtradas
function updateSwitchRackPosOptions(rack_id, office_id) {
  updateOptions('/sh/ajax/load_switch_rack_pos/', {
    'rack_id': rack_id,
    'office_id': office_id
  }, $('select[name="switch_rack_pos"]'), $('#id_switch_rack_pos').data('preselected'));
}

// Función para actualizar números de serie de switches filtrados
// function updateSwitchSerialNOptions(brand_id, office_id) {
//   updateOptions('/sh/ajax/load_switch_serial_n/', {
//     'brand_id': brand_id,
//     'office_id': office_id
//   }, $('select[name="switch_serial_n"]'), $('#id_switch_serial_n').data('preselected'));
// }

function updateSerialNumberOptions(dev_type, brand_id, office_id) {
  updateOptions('/sh/ajax/load_device_serial_n/', {
      'dev_type_name': dev_type,
      'brand_id': brand_id,
      'office_id': office_id
  }, $('select[name="device_serial_n"]'));
  updateOptions('/sh/ajax/load_switch_serial_n/', {
      'brand_id': brand_id,
      'office_id': office_id
  }, $('select[name="switch_serial_n"]'));
}



// Función para actualizar modelos (switches) filtrados (con office_id)
function updateSwitchOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'switch',
    'office_id': office_id
  }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
}

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/move/list';
    }, actionType);
  });
}





