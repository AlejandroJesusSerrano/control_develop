$(document).ready(function() {
  $('.select2').select2({ theme: 'bootstrap' });

  // ========== INICIALIZAR DATEPICKER ==========
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

  // ========== CAMBIO DE OFICINA ==========
  $('select[name="office"]').off('change').on('change', function() {
    const office_id = $(this).val();
    const dev_type_val = $('select[name="dev_type"]').val() || '';
    const isSwitch = (dev_type_val.toUpperCase() === 'SWITCH');
    const usage = isSwitch ? 'switch' : 'device';

    if (office_id) {
      // 1) AJAX: cargar provincia/localidad
      $.ajax({
        url: '/sh/ajax/load_province_location/',
        type: 'POST',
        data: { 'office_id': office_id },
        dataType: 'json',
        success: function(data) {
          if (!data.error) {
            $('select[name="province"]').val(data.province_id).trigger('change.select2');
            $('select[name="location"]').val(data.location_id).trigger('change.select2');
            $('#id_office').select2('destroy').select2({ theme: 'bootstrap' });
          } else {
            console.error('Error: ', data.error);
          }
        },
        error: function(xhr, status, error) {
          console.error('AJAX Error: ', status, error);
        }
      });

      // 2) Filtrar racks, brand, ip, serial, switch, device
      updateSwitchOptions(dev_type_val, null, office_id);
      updateDeviceOptions(dev_type_val, null, office_id);
      updateRackOptions(office_id);
      updateBrandOptions(dev_type_val, usage, office_id);
      updateIpOptions(dev_type_val, usage, office_id);
      updateSerialNumberOptions(dev_type_val, null, office_id);
      updateDevTypeOptions(office_id)

      // 3) Cargar empleados
      if ($('#id_employee').length > 0) {
        updateOptions(
          '/sh/ajax/load_employee/',
          { 'office_id': office_id },
          $('select[name="employee"]'),
          $('#id_employee').data('preselected')
        );
      }
    }
  });

  // ========== CAMBIO DE TIPO DE DISPOSITIVO (dev_type) ==========
  $('select[name="dev_type"]').off('change').on('change', function() {
    // dev_type_id es el valor real del <option>, EJ: "6"
    const dev_type_id = $(this).val() || '';
    const office_id = $('select[name="office"]').val() || '';

    // Tomar la <option> seleccionada para leer data-devtype
    const $optionSel = $(this).find(`option[value="${dev_type_id}"]`);
    // dev_type_text será "SWITCH", "PC", etc.
    const dev_type_text = $optionSel.data('devtype') || '';

    // Saber si es Switch
    const isSwitch = (dev_type_text.toUpperCase() === 'SWITCH');
    const usage = isSwitch ? 'switch' : 'device';

    // Filtrar brand, IP, serial, etc. (pasando dev_type_id como antes)
    updateBrandOptions(dev_type_id, usage, office_id);
    updateIpOptions(dev_type_id, usage, office_id);
    updateSerialNumberOptions(dev_type_id, null, office_id);

    // Filtra Switch/DeviceModel
    if (isSwitch) {
      updateSwitchOptions(dev_type_id, null, office_id);
      // habilitar Switch
      $('select[name="switch"], select[name="switch_serial_n"]').prop('disabled', false);
      $('select[name="rack"], select[name="switch_rack_pos"]').prop('disabled', false);
      // deshabilitar Device
      $('select[name="device"], select[name="device_serial_n"]')
        .prop('disabled', true)
        .val('')
        .trigger('change');
    } else {
      updateModelOptions(dev_type_id, null, office_id);
      // habilitar Device
      $('select[name="device"], select[name="device_serial_n"]').prop('disabled', false);
      // deshabilitar Switch
      $('select[name="switch"], select[name="switch_serial_n"]')
        .prop('disabled', true)
        .val('')
        .trigger('change');
      $('select[name="rack"], select[name="switch_rack_pos"]')
        .prop('disabled', true)
        .val('')
        .trigger('change');
    }
  });

  // ========== CAMBIO DE MARCA ==========
  $('select[name="brand"]').off('change').on('change', function() {
    const brand_id = $(this).val();
    const dev_type_val = $('select[name="dev_type"]').val();
    const office_id = $('select[name="office"]').val();
    updateSerialNumberOptions(dev_type_val, brand_id, office_id);
  });

  // ========== BOTÓN "FILTRAR DISPOSITIVOS" ==========
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

  // ========== BOTÓN "FILTRAR OFICINAS Y EMPLEADOS" ==========
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

  // ========== INICIALIZAR ENVÍO DE FORMULARIO ==========
  initializeFormSubmission('#myform', 'add'); // O 'edit' según tu caso

});


/* ================================================================
 * FUNCIONES AUXILIARES PARA LLAMADAS AJAX
 * ================================================================ */

function updateSwitchOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_switch/', {
    dev_type_val: dev_type_val,
    brand_id: brand_id,
    office_id: office_id
  }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
}

function updateDeviceOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_device/', {
    dev_type_val: dev_type_val,
    brand_id: brand_id,
    office_id: office_id
  }, $('select[name="device"]'), $('#id_device').data('preselected'));
}

// Marca
function updateBrandOptions(dev_type_val, usage, office_id) {
  updateOptions('/sh/ajax/load_brand/', {
    'dev_type_name': dev_type_val,
    'usage': usage,
    'office_id': office_id
  }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
}

// IP
function updateIpOptions(dev_type_val, usage, office_id) {
  updateOptions('/sh/ajax/load_ip/', {
    'dev_type_name': dev_type_val,
    'usage': usage,
    'office_id': office_id
  }, $('select[name="ip"]'), $('#id_ip').data('preselected'));
}

// Serial
function updateSerialNumberOptions(dev_type, brand_id, office_id) {
  // Dispositivos
  updateOptions('/sh/ajax/load_device_serial_n/', {
    'dev_type_name': dev_type,
    'brand_id': brand_id,
    'office_id': office_id
  }, $('select[name="device_serial_n"]'));

  // Switch
  updateOptions('/sh/ajax/load_switch_serial_n/', {
    'brand_id': brand_id,
    'office_id': office_id
  }, $('select[name="switch_serial_n"]'));
}

// Modelos device
function updateModelOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'device',
    'office_id': office_id
  }, $('select[name="device"]'), $('#id_device').data('preselected'));
}

// Modelos switch
function updateSwitchOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'switch',
    'office_id': office_id
  }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
}

// Racks
function updateRackOptions(office_id) {
  updateOptions('/sh/ajax/load_rack/', {
    'office_id': office_id
  }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
}

// Rack Pos
function updateSwitchRackPosOptions(rack_id, office_id) {
  updateOptions('/sh/ajax/load_switch_rack_pos/', {
    'rack_id': rack_id,
    'office_id': office_id
  }, $('select[name="switch_rack_pos"]'), $('#id_switch_rack_pos').data('preselected'));
}

function updateDevTypeOptions(office_id, dev_type_id) {
  updateOptions(
    '/sh/ajax/load_dev_type/',
    { 'office_id': office_id },
    $('select[name="dev_type"]'),
    dev_type_id
  );
}


function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    submit_with_ajax(
      $(this).attr('action'),
      formData,
      function() {
        console.log('Formulario enviado y procesado con éxito');
        window.location.href = '/sh/move/list';
      },
      actionType
    );
  });
}



// $(document).ready(function() {
//   $('.select2').select2({ theme: 'bootstrap' });

//   // --- INICIALIZAR DATEPICKER ---
//   $('#id_suply_date_in_input').datepicker({
//     format: 'dd/mm/yyyy',
//     autoclose: true,
//     todayHighlight: true,
//     language: 'es',
//     orientation: 'auto',
//     zIndexOffset: 1050
//   }).on('changeDate', function(e) {
//     $('#id_suply_date_in_input').val(e.format('dd/mm/yyyy'));
//   });

//   $('#id_suply_date_in_button').on('click', function() {
//     $('#id_suply_date_in_input').datepicker('show');
//   });

//   const dev_type = $('select[name="dev_type"]').val() || '';
//   const isSwitch = (dev_type.toUpperCase() === 'SWITCH');
//   if (isSwitch) {
//     updateSwitchOptions(dev_type, null, office_id);
//   } else {
//     updateModelOptions(dev_type, null, office_id);
//   }


//   $('select[name="office"]').off('change').on('change', function() {
//     const office_id = $(this).val();
//     const dev_type = $('select[name="dev_type"]').val() || '';
//     const isSwitch = (dev_type.toUpperCase() === 'SWITCH');
//     const usage = isSwitch ? 'switch' : 'device';

//     if (office_id) {
//       // 1) AJAX para cargar provincia/localidad
//       $.ajax({
//         url: '/sh/ajax/load_province_location/',
//         type: 'POST',
//         data: { 'office_id': office_id },
//         dataType: 'json',
//         success: function(data) {
//           if (!data.error) {
//             // Actualiza selects de provincia, location
//             $('select[name="province"]').val(data.province_id).trigger('change.select2');
//             $('select[name="location"]').val(data.location_id).trigger('change.select2');
//             // Reinicia el office select2
//             $('#id_office').select2('destroy').select2({ theme: 'bootstrap' });
//           } else {
//             console.error('Error: ', data.error);
//           }
//         },
//         error: function(xhr, status, error) {
//           console.error('AJAX Error: ', status, error);
//         }
//       });

//       // 2) Filtrar racks, brand, ip, serial...
//       updateRackOptions(office_id);
//       updateBrandOptions(dev_type, usage, office_id);
//       updateIpOptions(dev_type, usage, office_id);
//       updateSerialNumberOptions(dev_type, null, office_id);

//       // 3) Cargar empleados
//       if ($('#id_employee').length > 0) {
//         updateOptions(
//           '/sh/ajax/load_employee/',
//           { 'office_id': office_id },
//           $('select[name="employee"]'),
//           $('#id_employee').data('preselected')
//         );
//       }

//       // 4) Si quieres también filtrar el <select> "Switch" o "Device" en base a la oficina:
//       //    -> Llama updateSwitchOptions(...) o updateModelOptions(...)
//       if (isSwitch) {
//         updateSwitchOptions(dev_type, null, office_id);
//       } else {
//         updateModelOptions(dev_type, null, office_id);
//       }
//     }
//   });

//   $('select[name="dev_type"]').off('change').on('change', function() {
//     const dev_type = $(this).val() || '';
//     const office_id = $('select[name="office"]').val() || '';
//     const isSwitch = (dev_type.toUpperCase() === 'SWITCH');
//     const usage = isSwitch ? 'switch' : 'device';

//     // Refiltra brand, ip, serial
//     updateBrandOptions(dev_type, usage, office_id);
//     updateIpOptions(dev_type, usage, office_id);
//     updateSerialNumberOptions(dev_type, null, office_id);

//     // Filtra Switch/Device
//     if (isSwitch) {
//       updateSwitchOptions(dev_type, null, office_id);
//     } else {
//       updateModelOptions(dev_type, null, office_id);
//     }

//     // Habilitar/deshabilitar
//     if (isSwitch) {
//       // habilita switch fields
//       $('select[name="switch"], select[name="switch_serial_n"]').prop('disabled', false);
//       $('select[name="switch_serial_n"]').prop('disabled', false);
//       $('select[name="rack"], select[name="switch_rack_pos"]').prop('disabled', false);
//       // deshabilita device
//       $('select[name="device"]').prop('disabled', true).val('').trigger('change');
//       $('select[name="device_serial_n"]').prop('disabled', true).val('').trigger('change');
//     } else {
//       // habilita device
//       $('select[name="device"]').prop('disabled', false);
//       $('select[name="device_serial_n"]').prop('disabled', false);
//       // deshabilita switch
//       $('select[name="switch"]').prop('disabled', true).val('').trigger('change');
//       $('select[name="switch_serial_n"]').prop('disabled', true).val('').trigger('change');
//       $('select[name="rack"], select[name="switch_rack_pos"]').prop('disabled', true).val('').trigger('change');
//     }
//   });

//   // --- CAMBIO DE MARCA ---
//   $('select[name="brand"]').on('change', function() {
//     const brand_id = $(this).val();
//     const dev_type = $('select[name="dev_type"]').val();
//     const office_id = $('select[name="office"]').val();
//     // Filtra nuevamente los N° de Serie con la marca elegida
//     updateSerialNumberOptions(dev_type, brand_id, office_id);
//   });

//   // --- Toggle para filtros de dispositivos ---
//   $('#toggle-device-filters').on('click', function(e) {
//     e.preventDefault();
//     const filterDeviceCards = $('#filter-device-cards');
//     filterDeviceCards.toggleClass('d-none');
//     $(this).toggleClass('active btn-primary btn-secondary');
//     if (filterDeviceCards.hasClass('d-none')) {
//       $(this).html('Filtrar Dispositivos <i class="fas fa-search"></i>');
//     } else {
//       $(this).html('Ocultar Filtros <i class="fas fa-times"></i>');
//     }
//   });

//   // --- Toggle para filtros de oficinas y empleados ---
//   $('#toggle-office-filters').on('click', function(e) {
//     e.preventDefault();
//     const filterOfficeCards = $('#filter-office-cards');
//     filterOfficeCards.toggleClass('d-none');
//     $(this).toggleClass('active btn-primary btn-secondary');
//     if (filterOfficeCards.hasClass('d-none')) {
//       $(this).html('Filtrar Oficinas y Empleados <i class="fa fa-filter"></i>');
//     } else {
//       $(this).html('Ocultar Filtros <i class="fas fa-times"></i>');
//     }
//   });

//   // --- Inicializar envío del formulario ---
//   initializeFormSubmission('#myform', 'edit');  // Ajusta si tu form es #myform o #MovementsForm
// });



// // Marca
// function updateBrandOptions(dev_type_val, usage, office_id) {
//   updateOptions('/sh/ajax/load_brand/', {
//     'dev_type_name': dev_type_val,
//     'usage': usage,
//     'office_id': office_id
//   }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
// }

// // IP
// function updateIpOptions(dev_type_val, usage, office_id) {
//   updateOptions('/sh/ajax/load_ip/', {
//     'dev_type_name': dev_type_val,
//     'usage': usage,
//     'office_id': office_id
//   }, $('select[name="ip"]'), $('#id_ip').data('preselected'));
// }

// // Serial
// function updateSerialNumberOptions(dev_type, brand_id, office_id) {
//   // Dispositivos
//   updateOptions('/sh/ajax/load_device_serial_n/', {
//     'dev_type_name': dev_type,
//     'brand_id': brand_id,
//     'office_id': office_id
//   }, $('select[name="device_serial_n"]'));
//   // Switch
//   updateOptions('/sh/ajax/load_switch_serial_n/', {
//     'brand_id': brand_id,
//     'office_id': office_id
//   }, $('select[name="switch_serial_n"]'));
// }

// // Modelos device
// function updateModelOptions(dev_type_val, brand_id, office_id) {
//   updateOptions('/sh/ajax/load_model/', {
//     'dev_type_name': dev_type_val,
//     'brand_id': brand_id,
//     'usage': 'device',
//     'office_id': office_id
//   }, $('select[name="device"]'), $('#id_device').data('preselected'));
// }

// // Modelos switch
// function updateSwitchOptions(dev_type_val, brand_id, office_id) {
//   updateOptions('/sh/ajax/load_model/', {
//     'dev_type_name': dev_type_val,
//     'brand_id': brand_id,
//     'usage': 'switch',
//     'office_id': office_id
//   }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
// }

// // Racks
// function updateRackOptions(office_id) {
//   updateOptions('/sh/ajax/load_rack/', {
//     'office_id': office_id
//   }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
// }

// // Rack Pos
// function updateSwitchRackPosOptions(rack_id, office_id) {
//   updateOptions('/sh/ajax/load_switch_rack_pos/', {
//     'rack_id': rack_id,
//     'office_id': office_id
//   }, $('select[name="switch_rack_pos"]'), $('#id_switch_rack_pos').data('preselected'));
// }

// function initializeFormSubmission(formSelector, actionType) {
//   $(formSelector).on('submit', function(e) {
//     e.preventDefault();
//     let formData = new FormData(this);
//     submit_with_ajax(
//       $(this).attr('action'),
//       formData,
//       function() {
//         console.log('Formulario enviado y procesado con éxito');
//         window.location.href = '/sh/move/list';
//       },
//       actionType
//     );
//   });
// }






