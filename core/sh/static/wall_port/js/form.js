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

  if ($('#id_province').length > 0) {
    $('select[name="province"]').on('change', function() {
      const province_id = $(this).val();
      updateLocationOptions(province_id);
      updatePortsFromProvince(province_id);
    });
  }

  if ($('#id_location').length > 0) {
    $('select[name="location"]').on('change', function() {
      const location_id = $(this).val();
      updateLocationReferedOptions(location_id);
      updatePortsFromLocation(location_id);
    });
  }

  if ($('#id_edifice_port').length > 0) {
    $('select[name="edifice_port"]').on('change', function(){
      const edifice_port_id = $(this).val();
      updateEdificePortsOptions(edifice_port_id);
    });
  }

  if ($('#id_loc_port').length > 0) {
    $('select[name="loc_port"]').on('change', function(){
      const loc_port_id = $(this).val();
      updateLocPortsOptions(loc_port_id);
    });
  }

  if ($('#id_office_port').length > 0) {
    $('select[name="office_port"]').on('change', function(){
      const office_port_id = $(this).val();
      updateOfficePortsOptions(office_port_id);
    });
  }

  if ($('#id_rack_port').length > 0) {
    $('select[name="rack_port"]').on('change', function(){
      const rack_port_id = $(this).val();
      updateRackPortsOptions(rack_port_id);
    });
  }

  if ($('#id_patchera').length > 0) {
    $('select[name="patchera"]').on('change', function(){
      const patchera_id = $(this).val();
      if (patchera_id) {
        updateOptions('/sh/ajax/load_patch_ports/', {
          'patchera_id': patchera_id,
        }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));

        $('select[name="switch"]').val(null).trigger('change');
        $('select[name="switch_port_in"]').val(null).trigger('change');
        $('select[name="switch_port_in"]').closest('.form-group').hide();
      } else {
        $('select[name="switch_port_in"]').closest('.form-group').show();
      }
    });
  }

  if ($('#id_switch').length > 0) {
    $('select[name="switch"]').on('change', function(){
      const switch_id = $(this).val();
      if (switch_id) {
        updateOptions('/sh/ajax/load_switch_port/', {
          'switch_id': switch_id,
        }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

        $('select[name="patchera"]').val(null).trigger('change');
        $('select[name="patch_port_in"]').val(null).trigger('change');
        $('select[name="patch_port_in"]').closest('.form-group').hide();
      } else {
        $('select[name="patch_port_in"]').closest('.form-group').show();
      }
    });
  }

  initializeFormSubmission('#myform', 'edit');

});




function updatePortsFromProvince(province_id) {
  if (province_id) {
    if ($('#id_location').length > 0) {
      updateOptions('/sh/ajax/load_location/', {
        'province_id': province_id
      }, $('select[name="location"]'), $('#id_location').data('preselected'));
    }

    if ($('#id_edifice_port').length > 0) {
      updateOptions('/sh/ajax/load_edifices/', {
        'province_id': province_id
      }, $('select[name="edifice_port"]'), $('#id_edifice_port').data('preselected'));
    }

    if ($('#id_loc_port').length > 0) {
      updateOptions('/sh/ajax/load_loc/', {
        'province_id': province_id
      }, $('select[name="loc_port"]'), $('#id_loc_port').data('preselected'));
    }

    if ($('#id_office_port').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'province_id': province_id
      }, $('select[name="office_port"]'), $('#id_office_port').data('preselected'));
    }

    if ($('#id_rack_port').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'province_id': province_id
      }, $('select[name="rack_port"]'), $('#id_rack_port').data('preselected'));
    }
  }
}

function updatePortsFromLocation(location_id) {
  if (location_id) {
    if ($('#id_edifice_port').length > 0) {
      updateOptions('/sh/ajax/load_edifices/', {
        'location_id': location_id
      }, $('select[name="edifice_port"]'), $('#id_edifice_port').data('preselected'));
    }

    if ($('#id_loc_port').length > 0) {
      updateOptions('/sh/ajax/load_loc/', {
        'location_id': location_id
      }, $('select[name="loc_port"]'), $('#id_loc_port').data('preselected'));
    }

    if ($('#id_office_port').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'location_id': location_id
      }, $('select[name="office_port"]'), $('#id_office_port').data('preselected'));
    }

    if ($('#id_rack_port').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'location_id': location_id
      }, $('select[name="rack_port"]'), $('#id_rack').data('preselected'));
    }
  }
}

function updateEdificePortsOptions(edifice_port_id) {
  if (edifice_port_id) {
    if ($('#id_loc_port').length > 0) {
      updateOptions('/sh/ajax/load_loc/', {
        'edifice_id': edifice_port_id
      }, $('select[name="loc_port"]'), $('#id_loc_port').data('preselected'));
    }

    if ($('#id_office_port').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="office_port"]'), $('#id_office_port').data('preselected'));
    }

    if ($('#id_wall_port_in').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }

    if ($('#id_rack_port').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="rack_port"]'), $('#id_rack_port').data('preselected'));
    }

    if ($('#id_switch').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
    }

    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }

    if ($('#id_patchera_port').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="patchera_port"]'), $('#id_patchera_port').data('preselected'));
    }

    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'edifice_id': edifice_port_id,
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }
  }
}

function updateLocPortsOptions(loc_port_id) {
  if (loc_port_id){
    if ($('#id_office_port').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'loc_id': loc_port_id
      }, $('select[name="office_port"]'), $('#id_office_port').data('preselected'));
    }

    if ($('#id_wall_port_in').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'loc_id': loc_port_id
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }

    if ($('#id_rack_port').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'loc_id': loc_port_id
      }, $('select[name="rack_port"]'), $('#id_rack_port').data('preselected'));
    }

    if ($('#id_switch').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'loc_id': loc_port_id
      }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
    }

    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'loc_id': loc_port_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }

    if ($('#id_patchera').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'loc_id': loc_port_id
      }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
    }

    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'loc_id': loc_port_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }
  }
}

function updateOfficePortsOptions(office_port_id) {
  if (office_port_id){
    if ($('#id_wall_port').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'office_id': office_port_id
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }

    if ($('#id_rack_port').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'office_id': office_port_id
      }, $('select[name="rack_port"]'), $('#id_rack_port').data('preselected'));
    }

    if ($('#id_switch').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'office_id': office_port_id
      }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
    }

    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'office_id': office_port_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }

    if ($('#id_patchera').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'office_id': office_port_id
      }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
    }
  }
}


function updateRackPortsOptions(rack_port_id) {
  if (rack_port_id){
    if ($('#id_patchera_port').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'rack_id': rack_port_id
      }, $('select[name="patchera_port"]'), $('#id_patchera_port').data('preselected'));
    }

    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'rack_id': rack_port_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }

    if ($('#id_switch').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'rack_id': rack_port_id
      }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
    }

    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'rack_id': rack_port_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }
  }
}

function updatePatcheraPortsOptions(patchera_id) {
  updateOptions('/sh/ajax/load_patch_ports/', {
    'patchera_id': patchera_id
  }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
}

function updateSwitchPortsOptions(switch_id) {
  updateOptions('/sh/ajax/load_switch_port/', {
    'switch_id': switch_id
  }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
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
