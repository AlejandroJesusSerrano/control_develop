$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  updateSwitchBrandOptions();

  if ($('#id_brand').length > 0) {
    $('select[name="brand"]').on('change', function() {
    const brand_id = $(this).val();
    updateSwitchModelOptions(brand_id);
    });
  }

  if ($('#id_province').length > 0) {
    $('select[name="province"]').on('change', function(){
      updateLocationOptions(province_id);
    });
  }

  if ($('#id_location_switch').length > 0) {
    $('select[name="location"]').on('change', function(){
      const location_id = $(this).val();
      updateLocationReferedOptions(location_id)
    })
  }

  if ($('#id_edifice_switch').length > 0) {
    $('select[name="edifice"]').on('change', function(){
      const edifice_id = $(this).val();
      updateEdificeOptions(edifice_id);
    })
  }

  if ($('#id_dependency_switch').length > 0) {
    $('select[name="dependency"]').on('change', function(){
      const dependency_id = $(this).val();
      updateDependencyOptions(dependency_id);
    })
  }

  if ($('#id_loc_switch').length > 0) {
    $('select[name="loc"]').on('change', function(){
      const loc_id = $(this).val();
      updateLocOptions(loc_id);
    })
  }

  if ($('#id_office_switch').length > 0) {
    $('select[name="office"]').on('change', function(){
      const office_id = $(this).val();
      updateOfficeOptions(office_id);
    })
  }

  $('#toggle-office-filters').on('click', function (e) {
    e.preventDefault();
    const filterLocCards = $('#filter-office-cards')
    filterLocCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterLocCards.hasClass('d-none')) {
      $(this).html('Filtros de oficinas <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });

  $('#toggle-ports-filters').on('click', function (e) {
    e.preventDefault();
    const filterPortCards = $('#filter-port-cards')
    filterPortCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterPortCards.hasClass('d-none')) {
      $(this).html('Filtros para puertos <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });

  initializeFormSubmission('#myform', 'edit');

});

function updateSwitchBrandOptions() {
  const dev_type_name = 'SWITCH';
  updateOptions('/sh/ajax/load_brand/', {
    'dev_type_name': dev_type_name
  }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
}

function updateSwitchModelOptions(brand_id) {
  const dev_type_name = 'SWITCH';
  updateOptions('/sh/ajax/load_model/', {
    'brand_id': brand_id,
    'dev_type_name': dev_type_name
  }, $('select[name="model"]'), $('#id_model').data('preselected'));
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