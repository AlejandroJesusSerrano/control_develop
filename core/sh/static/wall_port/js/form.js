$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  $('select[name="province"]').on('change', function() {
    const province_id = $(this).val();
    clearSelects(['location', 'edifice', 'dependency', 'loc', 'office', 'rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in']);
    updateLocationOptions(province_id);
  });

  $('select[name="location"]').on('change', function() {
    const location_id = $(this).val();
    clearSelects(['edifice', 'dependency', 'loc', 'office', 'rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in']);
    if (location_id) {
      updateLocationRelatedOptions(location_id);
    }
  });

  $('select[name="edifice"]').on('change', function() {
    const edifice_id = $(this).val();
    clearSelects(['loc', 'office', 'rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in']);
    if (edifice_id) {
      updateDependencyOptions(edifice_id);
    }
  });

  $('select[name="dependency"]').on('change', function() {
    const dependency_id = $(this).val();
    const edifice_id = $('select[name="edifice"]').val();
    const location_id = $('select[name="location"]').val();

    clearSelects(['loc', 'office', 'rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in']);

    if (dependency_id) {
      if (edifice_id) {
        updateLocOptions(edifice_id, dependency_id);
      }
      else if (location_id) {
        updateOfficeOptions(null, dependency_id);
      }
      clearSelects(['office']);
    }
  });

  $('select[name="loc"]').on('change', function() {
    const loc_id = $(this).val();
    const dependency_id = $('select[name="dependency"]').val();

    clearSelects(['office', 'rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in']);

    if (loc_id && dependency_id) {
      updateOfficeOptions(loc_id, dependency_id);
    }
  });

  $('select[name="office_id"]').on('change', function() {
    const office_id = $(this).val();
    clearSelects(['rack', 'switch', 'switch_port_in', 'patchera', 'patch_port_in']);
    updateRackOptions(office_id)
  })

  $('select[name="rack"]').on('change', function(){
    const rack_id = $(this).val();
    clearSelects(['switch_in', 'switch_port_in', 'patchera_in', 'patch_port_in']);
    updateRackRelatedOptions(rack_id);
  })

  $('select[name="switch_in"]').on('change', function(){
    const switch_id = $(this).val();
    clearSelects(['switch_port_in']);
    UpdateSwitchPortOptions(switch_id);
  })

  $('select[name="patchera_in"]').on('change', function(){
    const patchera_id = $(this).val();
    clearSelects(['patch_port_in']);
    UpdatePatcheraPortOptions(patchera_id);
  })

  function clearSelects(fields) {
    fields.forEach(field => {
      $(`select[name="${field}"]`).empty().append('<option value="">----------</option>').trigger('change');
    });
  }

});

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

function updateRackOptions(office_id) {
  updateOptions('/sh/ajax/load_rack/', {
    'office_id': office_id,
  }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
}

function updateRackRelatedOptions(rack_id) {
  if (rack_id) {
    // Cargar switches
    updateOptions('/sh/ajax/load_switch/', {
      'rack_id': rack_id,
    }, $('select[name="switch_in"]'), $('#id_switch_in').data('preselected'));

    // Cargar patcheras
    updateOptions('/sh/ajax/load_patchera/', {
      'rack_id': rack_id
    }, $('select[name="patchera_in"]'), $('#id_patchera_in').data('preselected'));
  }
}

function updateSwitchPortOptions(switch_id) {
  updateOptions('/sh/ajax/load_switch_port/', {
    'switch_id': switch_id,
  }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
}

function updatePatcheraPortOptions(patchera_id) {
  updateOptions('/sh/ajax/load_patch_ports/', {
    'patchera_id': patchera_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
}

