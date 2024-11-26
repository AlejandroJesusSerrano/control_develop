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
    const province_id = $(this).val();
    updateLocationOptions(province_id);
  });

  $('select[name="location"]').on('change', function() {
    const location_id = $(this).val();
    if (location_id) {
      updateLocationRelatedOptions(location_id);
      // Limpiar selecciones dependientes
      clearSelects(['edifice', 'dependency', 'loc', 'office']);
    }
  });

  $('select[name="edifice"]').on('change', function() {
    const edifice_id = $(this).val();
    if (edifice_id) {
      updateDependencyOptions(edifice_id);
      clearSelects(['loc', 'office']);
    }
  });

  $('select[name="dependency"]').on('change', function() {
    const dependency_id = $(this).val();
    const edifice_id = $('select[name="edifice"]').val();
    const location_id = $('select[name="location"]').val();

    if (dependency_id) {
      // Si tenemos edificio, filtramos loc por edificio y dependency
      if (edifice_id) {
        updateLocOptions(edifice_id, dependency_id);
      }
      // Si no hay edificio pero hay location, podemos filtrar offices directamente
      else if (location_id) {
        updateOfficeOptions(null, dependency_id);
      }
      clearSelects(['office']);
    }
  });

  $('select[name="loc"]').on('change', function() {
    const loc_id = $(this).val();
    const dependency_id = $('select[name="dependency"]').val();
    if (loc_id && dependency_id) {
      updateOfficeOptions(loc_id, dependency_id);
    }
  });

  function clearSelects(fields) {
    fields.forEach(field => {
      $(`select[name="${field}"]`).empty().append('<option value="">----------</option>').trigger('change');
    });
  }

  initializeFormSubmission('#myform', 'edit');
});

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

function updateLocationOptions(province_id) {
  updateOptions('/sh/ajax/load_location/', {
    'province_id': province_id,
  }, $('select[name="location"]'), $('#id_location').data('preselected'));
}

function updateLocationRelatedOptions(location_id) {
  if (location_id) {
    // Cargar edificios
    updateOptions('/sh/ajax/load_edifices/', {
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));

    // Cargar dependencies iniciales basadas en location
    updateOptions('/sh/ajax/load_dependency/', {
      'location_id': location_id,
    }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
  }
}

function updateDependencyOptions(edifice_id) {
  if (edifice_id) {
    updateOptions('/sh/ajax/load_dependency/', {
      'edifice_id': edifice_id,
    }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
  }
}

function updateLocOptions(edifice_id, dependency_id) {
  const data = {
    'edifice_id': edifice_id
  };
  if (dependency_id) data.dependency_id = dependency_id;

  updateOptions('/sh/ajax/load_loc/', data,
    $('select[name="loc"]'),
    $('#id_loc').data('preselected')
  );
}

function updateOfficeOptions(loc_id, dependency_id) {
  const data = {
    'dependency_id': dependency_id
  };
  if (loc_id) data.loc_id = loc_id;

  updateOptions('/sh/ajax/load_office/', data,
    $('select[name="office"]'),
    $('#id_office').data('preselected')
  );
}