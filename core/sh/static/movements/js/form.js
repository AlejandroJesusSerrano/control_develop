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

  // Utilidad: obtener el valor actual de "office"
  function getOfficeId() {
    return $('select[name="office"]').val() || '';
  }

  // ---------- EVENTO: CAMBIO DE OFICINA ----------
  $('select[name="office"]').off('change').on('change', function() {
    let office_id = $(this).val();
    if (office_id) {
      // Actualizar provincia y localidad según la oficina
      $.ajax({
        url: '/sh/ajax/load_province_location/',
        type: 'POST',
        data: { office_id: office_id },
        dataType: 'json',
        success: function(data) {
          if (!data.error) {
            $('select[name="province"]').val(data.province_id).trigger('change.select2');
            $('select[name="location"]').val(data.location_id).trigger('change.select2').trigger('change');
            $('#id_office').select2('destroy').select2({ theme: 'bootstrap' });
          } else {
            console.error('Error en load_province_location:', data.error);
          }
        },
        error: function(xhr, status, error) {
          console.error('AJAX Error (load_province_location):', status, error);
        }
      });

      // Actualizar el select de dev_type (sin cambiar la selección actual si ya existe)
      updateDevTypeOptions(office_id);

      // Leer el valor actual de dev_type y demás filtros (si los hubiera)
      let dev_type_val = $('select[name="dev_type"]').val() || '';
      let d_brand_val = $('select[name="d_brand"]').val() || '';

      updateModelOptions(dev_type_val, d_brand_val, office_id);
      updateRackOptions(office_id);
    }
  });

  // ---------- EVENTO: CAMBIO DE TIPO DE DISPOSITIVO (dev_type) ----------
  $('select[name="dev_type"]').off('change').on('change', function() {
    let dev_type_val = $(this).val() || '';
    let dev_type_text = $(this).find('option:selected').text().trim();
    let isSwitch = (dev_type_text.toUpperCase() === 'SWITCH');
    let usage = isSwitch ? 'switch' : 'device';
    let office_id = getOfficeId();

    // Actualizar los filtros dependientes de dev_type
    updateBrandOptions(dev_type_val, usage, office_id);
    updateIpOptions(dev_type_val, usage, office_id);
    updateSerialNumberOptions(dev_type_val, null, office_id);
    if (usage === 'device') {
      let d_brand_val = $('select[name="d_brand"]').val() || '';
      updateModelOptions(dev_type_val, d_brand_val, office_id);
    }
  });

  // ---------- EVENTO: CAMBIO DE MARCA (d_brand) ----------
  $('select[name="d_brand"]').off('change').on('change', function() {
    let d_brand_val = $(this).val();
    let dev_type_val = $('select[name="dev_type"]').val() || '';
    let office_id = getOfficeId();
    updateDeviceSerialNOptions(dev_type_val, d_brand_val, office_id);
    updateModelOptions(dev_type_val, d_brand_val, office_id);
    updateIpOptions(dev_type_val, 'device', office_id);
  });

  // ---------- EVENTO: CAMBIO DE IP (d_ip) ----------
  $('select[name="d_ip"]').off('change').on('change', function() {
    // Si el usuario inicia filtrado por IP, actualizamos los siguientes (modelo y serial)
    let dev_type_val = $('select[name="dev_type"]').val() || '';
    let d_brand_val = $('select[name="d_brand"]').val() || '';
    let office_id = getOfficeId();
    updateModelOptions(dev_type_val, d_brand_val, office_id);
    updateDeviceSerialNOptions(dev_type_val, d_brand_val, office_id);
  });

  // ---------- EVENTO: CAMBIO DE DEVICE (device) ----------
  $('select[name="device"]').off('change').on('change', function() {
    // El usuario ya seleccionó un dispositivo; aquí podrías realizar acciones adicionales si lo requieres.
  });

  // ---------- TOGGLES ----------
  $('#toggle-device-filters').on('click', function(e) {
    e.preventDefault();
    let filterDeviceCards = $('#filter-device-cards');
    filterDeviceCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    $(this).html(filterDeviceCards.hasClass('d-none')
      ? 'Filtrar Dispositivo <i class="fa fa-search"></i>'
      : 'Ocultar Filtros <i class="fas fa-times"></i>');
  });
  $('#toggle-office-filters').on('click', function(e) {
    e.preventDefault();
    let filterOfficeCards = $('#filter-office-cards');
    filterOfficeCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    $(this).html(filterOfficeCards.hasClass('d-none')
      ? 'Filtrar Oficinas y Empleados <i class="fa fa-filter"></i>'
      : 'Ocultar Filtros <i class="fas fa-times"></i>');
  });

  // ---------- INICIALIZAR ENVÍO DEL FORMULARIO ----------
  initializeFormSubmission('#myform', 'add');
});


// -------------------- FUNCIONES AUXILIARES -------------------- //

function updateBrandOptions(dev_type_val, usage, office_id) {
  updateOptions('/sh/ajax/load_brand/', {
    'dev_type_name': dev_type_val,
    'usage': usage,
    'office_id': office_id
  }, $('select[name="d_brand"]'), $('select[name="d_brand"]').data('preselected'));
}

function updateIpOptions(dev_type_val, usage, office_id) {
  updateOptions('/sh/ajax/load_ip/', {
    'dev_type_name': dev_type_val,
    'usage': usage,
    'office_id': office_id
  }, $('select[name="d_ip"]'), $('select[name="d_ip"]').data('preselected'));
}

function updateModelOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'device',
    'office_id': office_id
  }, $('select[name="device"]'), $('select[name="device"]').data('preselected'));
}

function updateSwitchOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'switch',
    'office_id': office_id
  }, $('select[name="switch"]'), $('select[name="switch"]').data('preselected'));
}

function updateDeviceSerialNOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_device_serial_n/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'office_id': office_id
  }, $('select[name="device_serial_n"]'), $('select[name="device_serial_n"]').data('preselected'));
}

function updateSwitchSerialNOptions(brand_id, office_id) {
  updateOptions('/sh/ajax/load_switch_serial_n/', {
    'brand_id': brand_id,
    'office_id': office_id
  }, $('select[name="switch_serial_n"]'), $('select[name="switch_serial_n"]').data('preselected'));
}

function updateSwitchRackPosOptions(rack_id, office_id) {
  updateOptions('/sh/ajax/load_switch_rack_pos/', {
    'rack_id': rack_id,
    'office_id': office_id
  }, $('select[name="switch_rack_pos"]'), $('select[name="switch_rack_pos"]').data('preselected'));
}

function updateSerialNumberOptions(dev_type_val, brand_id, office_id) {
  // Actualiza ambos seriales
  updateDeviceSerialNOptions(dev_type_val, brand_id, office_id);
  updateSwitchSerialNOptions(brand_id, office_id);
}

function updateDevTypeOptions(office_id) {
  let current = $('select[name="dev_type"]').data('preselected') || $('select[name="dev_type"]').val() || '';
  updateOptions('/sh/ajax/load_dev_type/', { office_id: office_id }, $('select[name="dev_type"]'), current);
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
//   // Inicializar todos los selects con select2
//   $('.select2').select2({ theme: 'bootstrap' });

//   // ---------- INICIALIZAR DATEPICKER ----------
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

//   // Utilidad: obtener el valor actual de "office"
//   function getOfficeId() {
//     return $('select[name="office"]').val() || '';
//   }

//   // ---------- EVENTO: CAMBIO DE OFICINA ----------
//   $('select[name="office"]').off('change').on('change', function() {
//     let office_id = $(this).val();
//     if (office_id) {
//       // Actualizar provincia y localidad según la oficina
//       $.ajax({
//         url: '/sh/ajax/load_province_location/',
//         type: 'POST',
//         data: { office_id: office_id },
//         dataType: 'json',
//         success: function(data) {
//           if (!data.error) {
//             $('select[name="province"]').val(data.province_id).trigger('change.select2');
//             $('select[name="location"]').val(data.location_id).trigger('change.select2').trigger('change');
//             $('#id_office').select2('destroy').select2({ theme: 'bootstrap' });
//           } else {
//             console.error('Error en load_province_location:', data.error);
//           }
//         },
//         error: function(xhr, status, error) {
//           console.error('AJAX Error (load_province_location):', status, error);
//         }
//       });

//       // **No actualizamos el select de dev_type** para conservar la selección.
//       let dev_type_val = $('select[name="dev_type"]').val() || '';
//       let dev_type_text = $('select[name="dev_type"] option:selected').text().trim();
//       let isSwitch = (dev_type_text.toUpperCase() === 'SWITCH');
//       let usage = isSwitch ? 'switch' : 'device';
//       let brand_id = $('select[name="brand"]').val();

//       // Actualizar los demás filtros en cascada:
//       if (isSwitch) {
//         updateSwitchOptions(dev_type_val, brand_id, office_id);
//         updateBrandOptions(dev_type_val, 'switch', office_id);
//         updateIpOptions(dev_type_val, 'switch', office_id);
//         updateSwitchSerialNOptions(brand_id, office_id);
//       } else {
//         updateModelOptions(dev_type_val, brand_id, office_id);
//         updateBrandOptions(dev_type_val, 'device', office_id);
//         updateIpOptions(dev_type_val, 'device', office_id);
//         updateDeviceSerialNOptions(dev_type_val, brand_id, office_id);
//       }
//       updateRackOptions(office_id);
//     }
//   });


//   if ($('id_d_brand').length > 0) {
//     $('select[name="d_brand"]').on('change', function() {
//       const d_brand_id = $(this).val();
//       updateDeviceOptions(d_brand_id);
//     });
//   }

//   $('select[name="dev_type"]').on('change', function() {
//     const dev_type = $(this).val();
//     const d_brand_id = $('select[name="d_brand"]').val();
//     updateDevBrandOptions(dev_type, d_brand_id);
//     updateDeviceOptions(dev_type, null);
//   });

//   $('select[name="d_brand"]').on('change', function() {
//     const d_brand_id = $(this).val();
//     const dev_type = $('select[name="dev_type"]').val();
//     updateDeviceOptions(dev_type, d_brand_id);
//   });


//   // ---------- TOGGLES ----------
//   $('#toggle-device-filters').on('click', function(e) {
//     e.preventDefault();
//     let filterDeviceCards = $('#filter-device-cards');
//     filterDeviceCards.toggleClass('d-none');
//     $(this).toggleClass('active btn-primary btn-secondary');
//     $(this).html(filterDeviceCards.hasClass('d-none')
//       ? 'Filtrar Dispositivos <i class="fas fa-search"></i>'
//       : 'Ocultar Filtros <i class="fas fa-times"></i>');
//   });
//   $('#toggle-switch-filters').on('click', function(e) {
//     e.preventDefault();
//     let filterSwitchCards = $('#filter-switch-cards');
//     filterSwitchCards.toggleClass('d-none');
//     $(this).toggleClass('active btn-primary btn-secondary');
//     $(this).html(filterSwitchCards.hasClass('d-none')
//       ? 'Filtrar Switches <i class="fas fa-search"></i>'
//       : 'Ocultar Filtros <i class="fas fa-times"></i>');
//   });
//   $('#toggle-office-filters').on('click', function(e) {
//     e.preventDefault();
//     let filterOfficeCards = $('#filter-office-cards');
//     filterOfficeCards.toggleClass('d-none');
//     $(this).toggleClass('active btn-primary btn-secondary');
//     $(this).html(filterOfficeCards.hasClass('d-none')
//       ? 'Filtrar Oficinas y Empleados <i class="fa fa-filter"></i>'
//       : 'Ocultar Filtros <i class="fas fa-times"></i>');
//   });

//   // ---------- INICIALIZAR ENVÍO DEL FORMULARIO ----------
//   initializeFormSubmission('#myform', 'add');
// });


// function updateBrandOptions(dev_type) {
//   updateOptions('/sh/ajax/load_brands/', {
//     usage: 'device',
//     dev_type_name: dev_type,
//   }, $('select[name="d_brand"]'));
// }

// function updateDeviceOptions(dev_type, d_brand_id) {
//   updateOptions('/sh/ajax/load_devices/', {
//     usage: 'device',
//     dev_type_name: dev_type,
//     brand_id: d_brand_id,
//   }, $('select[name="device"]'));
// }

// function initializeFormSubmission(formSelector, actionType) {
//   $(formSelector).on('submit', function(e) {
//     e.preventDefault();
//     let formData = new FormData(this);
//     submit_with_ajax($(this).attr('action'), formData, function() {
//       console.log('Formulario enviado y procesado con éxito');
//       window.location.href = '/sh/switch/list';
//     }, actionType);
//   });
// }