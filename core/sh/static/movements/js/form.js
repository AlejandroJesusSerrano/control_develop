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

  // Utilidad: obtener el office_id actual del select
  function getOfficeId() {
    return $('select[name="office"]').val() || '';
  }

  // ---------- EVENTO: CAMBIO DE OFICINA ----------
  $('select[name="office"]').off('change').on('change', function() {
    let office_id = $(this).val();
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
            $('#id_office').select2('destroy').select2({ theme: 'bootstrap' });
          } else {
            console.error('Error: ', data.error);
          }
        },
        error: function(xhr, status, error) {
          console.error('AJAX Error (load_province_location):', status, error);
        }
      });

      // Importante: NO actualizar el select dev_type para conservar la selección.
      // Solo se leen sus valores para actualizar los demás filtros.
      const currentDevTypeVal = $('select[name="dev_type"]').val() || '';
      updateOptions(
        '/sh/ajax/load_dev_type/',
        { office_id: office_id },
        $('select[name="dev_type"]'),
        currentDevTypeVal
      );
      let dev_type_text = $('select[name="dev_type"] option:selected').text().trim();
      let isSwitch = (dev_type_text.toUpperCase() === 'SWITCH');
      let usage = isSwitch ? 'switch' : 'device';
      let brand_id = $('select[name="brand"]').val();

      if (isSwitch) {
        updateSwitchOptions(dev_type_val, brand_id, usage, office_id);
        updateBrandOptions(dev_type_val, usage, office_id);
        updateIpOptions(dev_type_val, usage, office_id);
        updateSwitchSerialNOptions(brand_id, office_id);
        updateSwitchRackPosOptions(dev_type_val, usage, office_id);
      } else {
        updateModelOptions(dev_type_val, brand_id, office_id);
        updateBrandOptions(dev_type_val, usage, office_id);
        updateIpOptions(dev_type_val, usage, office_id);
        updateDeviceSerialNOptions(dev_type_val, brand_id, office_id);
      }
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

    // Actualizar filtros dependientes sin modificar dev_type
    updateBrandOptions(dev_type_val, usage, office_id);
    updateIpOptions(dev_type_val, usage, office_id);
    updateSerialNumberOptions(dev_type_val, null, office_id);

    if (isSwitch) {
      // Para SWITCH: desactivar device y su serial
      $('select[name="device"]').val('').trigger('change.select2').prop('disabled', true);
      $('select[name="device_serial_n"]').val('').trigger('change.select2').prop('disabled', true);
      // Habilitar switch y sus campos
      $('select[name="switch"]').prop('disabled', false);
      $('select[name="switch_serial_n"]').prop('disabled', false);
      $('select[name="rack"]').prop('disabled', false);
      $('select[name="switch_rack_pos"]').prop('disabled', false);
      updateSwitchOptions(dev_type_val, null, office_id);
      updateSwitchSerialNOptions($('select[name="brand"]').val(), office_id);
    } else {
      // Para dispositivos que NO son SWITCH: desactivar campos exclusivos de switch
      $('select[name="switch"]').val('').trigger('change.select2').prop('disabled', true);
      $('select[name="switch_serial_n"]').val('').trigger('change.select2').prop('disabled', true);
      $('select[name="rack"]').val('').trigger('change.select2').prop('disabled', true);
      $('select[name="switch_rack_pos"]').val('').trigger('change.select2').prop('disabled', true);
      // Habilitar device y su serial
      $('select[name="device"]').prop('disabled', false);
      $('select[name="device_serial_n"]').prop('disabled', false);
      updateModelOptions(dev_type_val, null, office_id);
      updateDeviceSerialNOptions(dev_type_val, null, office_id);
    }
  });

  // ---------- EVENTO: CAMBIO DE MARCA ----------
  $('select[name="brand"]').off('change').on('change', function() {
    let brand_id = $(this).val();
    let dev_type_val = $('select[name="dev_type"]').val();
    let office_id = getOfficeId();
    let dev_type_text = $('select[name="dev_type"] option:selected').text().trim();
    if (dev_type_text.toUpperCase() === 'SWITCH') {
      updateSwitchOptions(dev_type_val, brand_id, office_id);
      updateSwitchSerialNOptions(brand_id, office_id);
    } else {
      updateModelOptions(dev_type_val, brand_id, office_id);
      updateDeviceSerialNOptions(dev_type_val, brand_id, office_id);
    }
  });

  // ---------- EVENTO: CAMBIO DE RACK (para switches) ----------
  $('select[name="rack"]').off('change').on('change', function() {
    let rack_id = $(this).val();
    let office_id = getOfficeId();
    if (rack_id && office_id) {
      updateSwitchRackPosOptions(rack_id, office_id);
    }
  });

  // ---------- TOGGLES ----------
  $('#toggle-device-filters').on('click', function(e) {
    e.preventDefault();
    let filterDeviceCards = $('#filter-device-cards');
    filterDeviceCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    if (filterDeviceCards.hasClass('d-none')) {
      $(this).html('Filtrar Dispositivos <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class="fas fa-times"></i>');
    }
  });
  $('#toggle-office-filters').on('click', function(e) {
    e.preventDefault();
    let filterOfficeCards = $('#filter-office-cards');
    filterOfficeCards.toggleClass('d-none');
    $(this).toggleClass('active btn-primary btn-secondary');
    if (filterOfficeCards.hasClass('d-none')) {
      $(this).html('Filtrar Oficinas y Empleados <i class="fa fa-filter"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class="fas fa-times"></i>');
    }
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
  }, $('select[name="brand"]'), $('select[name="brand"]').val());
}

function updateIpOptions(dev_type_val, usage, office_id) {
  updateOptions('/sh/ajax/load_ip/', {
    'dev_type_name': dev_type_val,
    'usage': usage,
    'office_id': office_id
  }, $('select[name="ip"]'), $('select[name="ip"]').val());
}

function updateModelOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'device',
    'office_id': office_id
  }, $('select[name="device"]'), $('select[name="device"]').val());
}

function updateSwitchOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'switch',
    'office_id': office_id
  }, $('select[name="switch"]'), $('select[name="switch"]').val());
}

function updateDeviceSerialNOptions(dev_type_val, brand_id, office_id) {
  updateOptions('/sh/ajax/load_device_serial_n/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'office_id': office_id
  }, $('select[name="device_serial_n"]'), $('select[name="device_serial_n"]').val());
}

function updateSwitchSerialNOptions(brand_id, office_id) {
  updateOptions('/sh/ajax/load_switch_serial_n/', {
    'brand_id': brand_id,
    'office_id': office_id
  }, $('select[name="switch_serial_n"]'), $('select[name="switch_serial_n"]').val());
}

function updateSwitchRackPosOptions(rack_id, office_id) {
  updateOptions('/sh/ajax/load_switch_rack_pos/', {
    'rack_id': rack_id,
    'office_id': office_id
  }, $('select[name="switch_rack_pos"]'), $('select[name="switch_rack_pos"]').val());
}

function updateSerialNumberOptions(dev_type, brand_id, office_id) {
  // Actualiza ambos seriales
  updateDeviceSerialNOptions(dev_type, brand_id, office_id);
  updateSwitchSerialNOptions(brand_id, office_id);
}

function updateDevTypeOptions(office_id, currentDevType) {
  updateOptions(
    '/sh/ajax/load_dev_type/',
    { 'office_id': office_id },
    $('select[name="dev_type"]'),
    currentDevType
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