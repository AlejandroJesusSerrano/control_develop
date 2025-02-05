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

  // Evento para dev_type: actualizar campos según el tipo seleccionado
  $('select[name="dev_type"]').on('change', function() {
    const dev_type_val = $(this).val();
    const dev_type_text = $('select[name="dev_type"] option:selected').text().trim().toUpperCase();

    if(dev_type_text === "SWITCH") {
      // Si es SWITCH: deshabilitar y limpiar 'device'
      $('select[name="device"]').val('').trigger('change.select2').prop('disabled', true);
      // Habilitar 'switch'
      $('select[name="switch"]').prop('disabled', false);
      // Actualizar marcas e ips para switches
      updateBrandOptions(dev_type_val, 'switch');
      updateIpOptions(dev_type_val, 'switch');
      // (Opcional) Si tienes un campo para actualizar modelos para switches,
      // podrías llamar a una función similar, por ejemplo:
      // updateSwitchOptions(dev_type_val, null);
    } else {
      // Si NO es SWITCH: deshabilitar y limpiar 'switch'
      $('select[name="switch"]').val('').trigger('change.select2').prop('disabled', true);
      // Habilitar 'device'
      $('select[name="device"]').prop('disabled', false);
      // Actualizar marcas e ips para dispositivos
      updateBrandOptions(dev_type_val, 'device');
      updateIpOptions(dev_type_val, 'device');
      // **Importante:** Actualizar también el select de dispositivo (modelos)
      updateModelOptions(dev_type_val, null);
    }
  });

  // Cuando se cambia la marca, refinar el filtro de modelos (dispositivos o switches según corresponda)
  $('select[name="brand"]').on('change', function() {
    const brand_id = $(this).val();
    const dev_type_val = $('select[name="dev_type"]').val();
    updateModelOptions(dev_type_val, brand_id);
  });

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
  initializeFormSubmission('#' + formId, 'edit');  // Asumiendo que formId se define en el template
});


// Función para actualizar marcas filtradas
function updateBrandOptions(dev_type_val, usage) {
  updateOptions('/sh/ajax/load_brand/', {
    'dev_type_name': dev_type_val,
    'usage': usage
  }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
}

// Función para actualizar IPs filtradas
function updateIpOptions(dev_type_val, usage) {
  updateOptions('/sh/ajax/load_ip/', {
    'dev_type_name': dev_type_val,
    'usage': usage
  }, $('select[name="ip"]'), $('#id_ip').data('preselected'));
}

// Función para actualizar modelos (dispositivos) filtrados
function updateModelOptions(dev_type_val, brand_id) {
  updateOptions('/sh/ajax/load_model/', {
    'dev_type_name': dev_type_val,
    'brand_id': brand_id,
    'usage': 'device'
  }, $('select[name="device"]'), $('#id_device').data('preselected'));
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



