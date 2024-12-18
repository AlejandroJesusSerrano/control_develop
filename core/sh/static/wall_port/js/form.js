$(document).ready(function () {
  $('.select2').select2({
    theme: 'bootstrap',
  });

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

  $('select[name="province"]').on('change', function(){
    const province_id = $(this).val();
    updateLocationOptions(province_id);
  });

  $('select[name="location"]').on('change', function(){
    const location_id = $(this).val();
    updateLocationReferedOptions(location_id)
  })

  $('select[name="edifice"]').on('change', function(){
    const edifice_id = $(this).val();
    updateEdificeOptions(edifice_id);
  })

  $('select[name="dependency"]').on('change', function(){
    const dependency_id = $(this).val();
    updateDependencyOptions(dependency_id);
  })

  $('select[name="loc"]').on('change', function(){
    const loc_id = $(this).val();
    updateLocOptions(loc_id);
  })

  $('select[name="office"]').on('change', function(){
    const office_id = $(this).val();
    updateOfficeOptions(office_id);
  })

  $('select[name="rack"]').on('change', function(){
    const rack_id = $(this).val();
    updateRackOptions(rack_id);
  })

  $('select[name="patchera"]').on('change', function(){
    const patchera_id = $(this).val();
    updatePatcheraOptions(patchera_id);
  })

  $('select[name="switch"]').on('change', function(){
    const switch_id = $(this).val();
    updateSwitchOptions(switch_id)
  })


  initializeFormSubmission('#myform', 'edit');

});




function updateLocationOptions(province_id) {
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));

    updateOptions('/sh/ajax/load_dependency/', {
      'province_id': province_id,
    }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));

    updateOptions('/sh/ajax/load_edifices/', {
      'province_id': province_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));

    updateOptions('/sh/ajax/load_loc/', {
      'province_id': province_id,
    }, $('select[name="loc"]'), $('#id_loc').data('preselected'));

    updateOptions('/sh/ajax/load_office/', {
      'province_id': province_id,
    }, $('select[name="office"]'), $('#id_office').data('preselected'));

    updateOptions('/sh/ajax/load_rack/', {
      'province_id': province_id,
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));

    updateOptions('/sh/ajax/load_switch/', {
      'province_id': province_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'province_id': province_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'province_id': province_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'province_id': province_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_location', '#id_dependency', '#id_edifice', '#id_loc', '#id_office', '#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
};

function updateLocationReferedOptions(location_id) {
  if (location_id) {
    updateOptions('/sh/ajax/load_dependency/', {
      'location_id': location_id,
    }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));

    updateOptions('/sh/ajax/load_edifices/', {
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));

    updateOptions('/sh/ajax/load_loc/', {
      'location_id': location_id,
    }, $('select[name="loc"]'), $('#id_loc').data('preselected'));

    updateOptions('/sh/ajax/load_office/', {
      'location_id': location_id,
    }, $('select[name="office"]'), $('#id_office').data('preselected'));

    updateOptions('/sh/ajax/load_rack/', {
      'location_id': location_id,
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));

    updateOptions('/sh/ajax/load_switch/', {
      'location_id': location_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'location_id': location_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'location_id': location_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'location_id': location_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_dependency', '#id_edifice', '#id_loc', '#id_office', '#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
};



function updateDependencyOptions(dependency_id) {
  if (dependency_id) {
    updateOptions('/sh/ajax/load_office/', {
      'dependency_id': dependency_id,
    }, $('select[name="office"]'), $('#id_office').data('preselected'));

    updateOptions('/sh/ajax/load_rack/', {
      'dependency_id': dependency_id,
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));

    updateOptions('/sh/ajax/load_switch/', {
      'dependency_id': dependency_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'dependency_id': dependency_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'dependency_id': dependency_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'dependency_id': dependency_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_office', '#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
}

function updateEdificeOptions(edifice_id) {
  if (edifice_id) {

    updateOptions('/sh/ajax/load_office/', {
      'edifice_id': edifice_id,
    }, $('select[name="office"]'), $('#id_office').data('preselected'));

    updateOptions('/sh/ajax/load_rack/', {
      'edifice_id': edifice_id,
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));

    updateOptions('/sh/ajax/load_switch/', {
      'edifice_id': edifice_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'edifice_id': edifice_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'edifice_id': edifice_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'edifice_id': edifice_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_loc', '#id_office', '#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
}

function updateLocOptions(loc_id) {
  if (loc_id) {

    updateOptions('/sh/ajax/load_rack/', {
      'loc_id': loc_id,
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));

    updateOptions('/sh/ajax/load_switch/', {
      'loc_id': loc_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'loc_id': loc_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'loc_id': loc_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'loc_id': loc_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_office', '#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
}

function updateOfficeOptions(office_id) {
  if (office_id) {

    updateOptions('/sh/ajax/load_rack/', {
      'office_id': office_id,
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));

    updateOptions('/sh/ajax/load_switch/', {
      'office_id': office_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'office_id': office_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'office_id': office_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'office_id': office_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
}

function updateRackOptions(rack_id) {
  if (rack_id) {

    updateOptions('/sh/ajax/load_switch/', {
      'rack_id': rack_id,
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

    updateOptions('/sh/ajax/load_switch_port/', {
      'rack_id': rack_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

    updateOptions('/sh/ajax/load_patchera/', {
      'rack_id': rack_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

    updateOptions('/sh/ajax/load_patch_ports/', {
      'rack_id': rack_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_rack', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
  }
}

function updateSwitchOptions(switch_id) {
  if (switch_id) {

    updateOptions('/sh/ajax/load_switch_port/', {
      'switch_id': switch_id,
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_switch_port_in'])
  }
}

function updatePatcheraOptions(patchera_id) {
  if (patchera_id) {

    updateOptions('/sh/ajax/load_patch_ports/', {
      'patchera_id': patchera_id,
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
  } else {
    clearDependentFields(['#id_patch_port_in'])
  }
}

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/wall_port/list/';
    }, actionType);
  });
}

