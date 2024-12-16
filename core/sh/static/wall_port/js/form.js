$(document).ready(function () {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  const selectMapping = {
    province: ['location', 'dependency', 'edifice', 'loc', 'office'],
    location: ['dependency', 'edifice', 'loc', 'office'],
    dependency: ['office'],
    edifice: ['loc', 'office'],
    loc: ['office'],
    rack: ['switch', 'switch_port_in', 'patchera', 'patch_port_in'],
    switch: ['switch_port_in'],
    patchera: ['patch_port_in']
  };

  $('select[name="province"], select[name="location"], select[name="dependency"], select[name="edifice"], select[name="loc"], select[name="office"], select[name="rack"], select[name="switch"], select[name="patchera"]').on('change', function () {
    const fieldName = $(this).attr('name');
    const fieldsToClear = selectMapping[fieldName] || [];
    clearDependentFields(fieldsToClear.map(field => `select[name="${field}"]`));

    switch (fieldName) {
      case 'province':
        updateLocationOptions();
        updateDependencyOptions();
        updateEdificeOptions();
        updateLocOptions();
        updateOfficeOptions();
        updateRackOptions();
        updateRackRelatedOptions();
        updateSwitchOfficeOptions();
        break;

      case 'location':
        updateDependencyOptions();
        updateEdificeOptions();
        updateLocOptions();
        updateOfficeOptions();
        updateRackOptions();
        updateRackRelatedOptions();
        updateSwitchOfficeOptions();
        break;

      case 'dependency':
        updateOfficeOptions();
        updateRackOptions();
        updateRackRelatedOptions();
        updateSwitchOfficeOptions();
        break;

      case 'edifice':
        updateLocOptions();
        updateOfficeOptions();
        updateRackOptions();
        updateRackRelatedOptions();
        updateSwitchOfficeOptions();
        break;

      case 'loc':
        updateOfficeOptions();
        updateRackOptions();
        updateRackRelatedOptions();
        updateSwitchOfficeOptions();
        break;

      case 'office':
        updateRackOptions();
        updateRackRelatedOptions();
        updateSwitchOfficeOptions();
        break;

      case 'rack':
        const rack_id = $(this).val();
        updateRackRelatedOptions(rack_id);
        break;

      case 'switch':
        const switch_id = $(this).val();
        updateSwitchPortOptions(switch_id);
        break;

      case 'patchera':
        const patchera_id = $(this).val();
        updatePatcheraPortOptions(patchera_id);
        break;
    }
  });

  initializeFormSubmission('#myform', 'edit');
});

function updateLocationOptions() {
  const { province_id } = getSelectedFilters();
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', { province_id }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
}

function updateDependencyOptions() {
  const { province_id, location_id } = getSelectedFilters();
  const data = location_id ? { location_id } : province_id ? { province_id } : {};
  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_dependency/', data, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
  }
}

function updateEdificeOptions() {
  const { province_id, location_id } = getSelectedFilters();
  const data = location_id ? { location_id } : province_id ? { province_id } : {};
  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_edifices/', data, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  }
}

function updateLocOptions() {
  const { province_id, location_id, edifice_id } = getSelectedFilters();
  const data = edifice_id ? { edifice_id } : location_id ? { location_id } : province_id ? { province_id } : {};
  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_loc/', data, $('select[name="loc"]'), $('#id_loc').data('preselected'));
  }
}

function updateOfficeOptions() {
  const { province_id, location_id, dependency_id, edifice_id, loc_id } = getSelectedFilters();
  const data = { province_id, location_id, dependency_id, edifice_id, loc_id };
  updateOptions('/sh/ajax/load_office/', filterNonEmpty(data), $('select[name="office"]'), $('#id_office').data('preselected'));
}

function updateSwitchOfficeOptions() {
  const { province_id, location_id, dependency_id, edifice_id, loc_id, office_id } = getSelectedFilters();
  const data = { province_id, location_id, dependency_id, edifice_id, loc_id, office_id };
  updateOptions('/sh/ajax/load_switch/', filterNonEmpty(data), $('select[name="switch"]'), $('#id_switch').data('preselected'));
}

function updateRackOptions() {
  const { province_id, location_id, edifice_id, dependency_id, loc_id, office_id } = getSelectedFilters(); // Obtener el ID de la oficina seleccionada
  let data = {}
  if (office_id) {
    data = {office_id}
  } else if (province_id) {
    data = {province_id}
  } else if (location_id) {
    data = {location_id}
  } else if (dependency_id) {
    data = {dependency_id}
  } else if (edifice_id) {
    data = {edifice_id}
  } else if (loc_id) {
    data = {loc_id}
  }

  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_rack/', data, $('select[name="rack"]'), $('#id_rack').data('preselected'));
  } else {
    $('select[name="rack"]').empty().append('<option value="">----------</option>').trigger('change')
  }
}

function updateRackRelatedOptions(rack_id) {
  if (rack_id) {
    updateOptions('/sh/ajax/load_switch/', { rack_id }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
    updateOptions('/sh/ajax/load_patchera/', { rack_id }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
  }
}

function updateSwitchPortOptions(switch_id) {
  if (switch_id) {
    updateOptions('/sh/ajax/load_switch_port/', { switch_id }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
  }
}

function updatePatcheraPortOptions(patchera_id) {
  if (patchera_id) {
    updateOptions('/sh/ajax/load_patch_ports/', { patchera_id }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  }
}

function filterNonEmpty(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([_, value]) => value));
}

function getSelectedFilters() {
  return {
    province_id: $('select[name="province"]').val(),
    location_id: $('select[name="location"]').val(),
    dependency_id: $('select[name="dependency"]').val(),
    edifice_id: $('select[name="edifice"]').val(),
    loc_id: $('select[name="loc"]').val(),
    office_id: $('select[name="office"]').val(),
    rack_id: $('select[name="rack"]').val(),
    switch_id: $('select[name="switch"]').val(),
    patchera_id: $('select[name="patchera"]').val(),
  };
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

