$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  updateBrandOptions();

  // Event handlers
  $('select[name="brand"]').on('change', function() {
    const brand_id = $(this).val();
    updateModelOptions(brand_id);
  });

  $('select[name="province"]').on('change', function() {

    clearSelects(['location', 'dependency', 'edifice', 'loc', 'office']);

    updateLocationOptions();
    updateDependencyOptions();
    updateEdificeOptions();
    updateLocOptions();
    updateOfficeOptions();
  });

  $('select[name="location"]').on('change', function() {

    clearSelects(['dependency', 'edifice', 'loc', 'office']);

    updateDependencyOptions();
    updateEdificeOptions();
    updateLocOptions();
    updateOfficeOptions();
  });

  $('select[name="dependency"]').on('change', function() {

    clearSelects(['office']);

    updateOfficeOptions();
  });


  $('select[name="edifice"]').on('change', function() {

    clearSelects(['loc', 'office']);

    updateLocOptions();
    updateOfficeOptions();
  });

  $('select[name="loc"]').on('change', function() {
    clearSelects(['office']);

    updateOfficeOptions();
  });

  initializeFormSubmission('#myform', 'edit');

});

function clearSelects(fields) {
  fields.forEach(field => {
    $(`select[name="${field}"]`)
    .empty()
    .append('<option value="">----------</option>')
    .trigger('change');
  });
}

function getSelectedFilters(){
  return {
    province_id: $('select[name="province"]').val(),
    location_id: $('select[name="location"]').val(),
    dependency_id: $('select[name="dependency"]').val(),
    edifice_id: $('select[name="edifice"]').val(),
    loc_id: $('select[name="loc"]').val()
  };
}

// Funciones de actualización
function updateBrandOptions() {
  const dev_type_name = 'SWITCH';
  updateOptions('/sh/ajax/load_brand/', {
    'dev_type_name': dev_type_name
  }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
}

function updateModelOptions(brand_id) {
  const dev_type_name = 'SWITCH';
  updateOptions('/sh/ajax/load_model/', {
    'brand_id': brand_id,
    'dev_type_name': dev_type_name
  }, $('select[name="model"]'), $('#id_model').data('preselected'));
}

function updateLocationOptions() {
  const { province_id } = getSelectedFilters();
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
}

function updateDependencyOptions() {
  const { province_id, location_id } = getSelectedFilters();
  let data = {};
  if (location_id) {
    data['location_id'] = location_id;
  } else if (province_id) {
    data['province_id'] = province_id;
  }
  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_dependency/', data,
      $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
  }
}

function updateEdificeOptions() {
  const { province_id, location_id } = getSelectedFilters();
  let data = {};
  if (location_id) data['location_id'] = location_id;
  else if (province_id) data['province_id'] = province_id;

  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_edifices/', data,
      $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  }
}

function updateLocOptions() {
  const { province_id, location_id, edifice_id } = getSelectedFilters();
  let data = {};
  // Prioridad: edifice > location > province
  if (edifice_id) {
    data['edifice_id'] = edifice_id;
  } else if (location_id) {
    data['location_id'] = location_id;
  } else if (province_id) {
    data['province_id'] = province_id;
  }

  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_loc/', data,
      $('select[name="loc"]'), $('#id_loc').data('preselected'));
  }
}

function updateOfficeOptions() {
  const { province_id, location_id, dependency_id, edifice_id, loc_id } = getSelectedFilters();

  let data = {};
  // Se envían todos los filtros disponibles al backend
  if (province_id) data['province_id'] = province_id;
  if (location_id) data['location_id'] = location_id;
  if (dependency_id) data['dependency_id'] = dependency_id;
  if (edifice_id) data['edifice_id'] = edifice_id;
  if (loc_id) data['loc_id'] = loc_id;

  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_office/', data,
      $('select[name="office"]'), $('#id_office').data('preselected'));
  }
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