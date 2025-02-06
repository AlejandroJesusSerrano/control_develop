$(document).ready(function() {
  $('.select2').select2({
      theme: 'bootstrap',
  });

  if ($('#id_edifice_ports').length > 0) {
      $('select[name="edifice_ports"]').on('change', function() {
          const edifice_ports_id = $(this).val();
          updateEdificePortsOptions(edifice_ports_id);
      });
  }

  if ($('#id_loc_ports').length > 0) {
      $('select[name="loc_ports"]').on('change', function() {
          const loc_ports_id = $(this).val();
          updateLocPortsOptions(loc_ports_id);
      });
  }

  if ($('#id_office_ports').length > 0) {
      $('select[name="office_ports"]').on('change', function() {
          const office_ports_id = $(this).val();
          updateOfficePortsOptions(office_ports_id);
      });
  }

  if ($('#id_rack_ports').length > 0) {
      $('select[name="rack_ports"]').on('change', function() {
          const rack_ports_id = $(this).val();
          updateRackPortsOptions(rack_ports_id);
      });
  }

  if ($('#id_switch_ports').length > 0) {
    $('select[name="switch_ports"]').on('change', function() {
      const switch_ports_id = $(this).val();
      if (switch_ports_id) {
        updateOptions('/sh/ajax/load_switch_port/', {
          'switch_id': switch_ports_id
        }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

        $('select[name="patchera_ports"]').val(null).trigger('change');
        $('select[name="patch_port_in"]').val(null).trigger('change');
        $('select[name="patch_port_in"]').closest('.form-group').hide();
      } else {
        $('select[name="patch_port_in"]').closest('.form-group').show();
      }
    });
  }

  if ($('#id_patchera_ports').length > 0) {
    $('select[name="patchera_ports"]').on('change', function() {
      const patchera_id = $(this).val();
      if (patchera_id){
        updateOptions('/sh/ajax/load_patch_ports/', {
          'patchera_id': patchera_id
        }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));

        $('select[name="switch_ports"]').val(null).trigger('change');
        $('select[name="switch_port_in"]').val(null).trigger('change');
        $('select[name="switch_port_in"]').closest('.form-group').hide();
      } else {
        $('select[name="switch_port_in"]').closest('.form-group').show();
      }
    });
  }



  if ($('#id_brand').length > 0) {
      $('select[name="brand"]').on('change', function() {
          const brand_id = $(this).val();
          updateModelOptions(brand_id);
      });
  }

  $('select[name="dev_type"]').on('change', function() {
      const dev_type = $(this).val();
      const brand_id = $('select[name="brand"]').val();
      updateBrandOptions(dev_type);
      updateModelOptions(dev_type, null);
  });

  $('select[name="brand"]').on('change', function() {
      const brand_id = $(this).val();
      const dev_type = $('select[name="dev_type"]').val();
      updateModelOptions(dev_type, brand_id);
  });


  $('#toggle-device-filters').on('click', function(e) {
    e.preventDefault();
    const filterLocCards = $('#filter-device-cards')
    filterLocCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterLocCards.hasClass('d-none')) {
        $(this).html('Filtros para Modelos de Dispositivos <i class="fas fa-search"></i>');
    } else {
        $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });


  $('#toggle-office-filters').on('click', function(e) {
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

  $('#toggle-ports-filters').on('click', function(e) {
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

function updateEdificePortsFromLocation(location_id) {
  console.log('updateEdificePortsFromLocation llamada con location_id: ', location_id);
  if (location_id) {

    if ($('#id_edifice_ports').length > 0) {
      updateOptions('/sh/ajax/load_edifices/', {
        'location_id': location_id
      }, $('select[name="edifice_ports"]'), $('#id_edifice_ports').data('preselected'));
    }

    if ($('#id_loc_ports').length > 0) {
      updateOptions('/sh/ajax/load_loc/', {
        'location_id': location_id
      }, $('select[name="loc_ports"]'), $('#id_loc_ports').data('preselected'));
    }

    if ($('#id_office_ports').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'location_id': location_id
      }, $('select[name="office_ports"]'), $('#id_office_ports').data('preselected'));
    }

    if ($('#id_rack_ports').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'location_id': location_id
      }, $('select[name="rack_ports"]'), $('#id_rack').data('preselected'));
    }

    if ($('#id_switch_ports').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'location_id': location_id
      }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
    }

    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'location_id': location_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }

    if ($('#id_patchera_ports').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'location_id': location_id
      }, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));
    }

    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'location_id': location_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }

    if ($('#id_wall_port_in').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'location_id': location_id
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }

  } else {

      clearDependentFields(['#id_edifice_ports', '#id_loc_ports', '#id_office_ports', '#id_rack_ports']);

  }
}

function updateEdificePortsOptions(edifice_ports_id) {
  if (edifice_ports_id) {
    if ($('#id_loc_ports').length > 0) {
      updateOptions('/sh/ajax/load_loc/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="loc_ports"]'), $('#id_loc_ports').data('preselected'));
    }
    if ($('#id_office_ports').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="office_ports"]'), $('#id_office_ports').data('preselected'));
    }
    if ($('#id_rack_ports').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="rack_ports"]'), $('#id_rack_ports').data('preselected'));
    }
    if ($('#id_switch_ports').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
    }
    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }
    if ($('#id_patchera_ports').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));
    }
    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }
    if ($('#id_wall_port_in').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'edifice_id': edifice_ports_id
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }
  } else {
    clearDependentFields(['#id_loc_ports', '#id_office_ports', '#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
  }
}

function updateLocPortsOptions(loc_ports_id) {
  if (loc_ports_id) {
    if ($('#id_office_ports').length > 0) {
      updateOptions('/sh/ajax/load_office/', {
        'loc_id': loc_ports_id
      }, $('select[name="office_ports"]'), $('#id_office_ports').data('preselected'));
    }
    if ($('#id_rack_ports').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'loc_id': loc_ports_id
      }, $('select[name="rack_ports"]'), $('#id_rack_ports').data('preselected'));
    }
    if ($('#id_switch_ports').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'loc_id': loc_ports_id
      }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
    }
    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'loc_id': loc_ports_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }
    if ($('#id_patchera_ports').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'loc_id': loc_ports_id
      }, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));
    }
    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'loc_id': loc_ports_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }
    if ($('#id_wall_port_in').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'loc_id': loc_ports_id
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }
  } else {
    clearDependentFields(['#id_office_ports', '#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
  }
}

function updateOfficePortsOptions(office_ports_id) {
  if (office_ports_id) {
    if ($('#id_rack_ports').length > 0) {
      updateOptions('/sh/ajax/load_rack/', {
        'office_id': office_ports_id
      }, $('select[name="rack_ports"]'), $('#id_rack_ports').data('preselected'));
    }
    if ($('#id_switch_ports').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'office_id': office_ports_id
      }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
    }
    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'office_id': office_ports_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }
    if ($('#id_patchera_ports').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'office_id': office_ports_id
      }, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));
    }
    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'office_id': office_ports_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }
    if ($('#id_wall_port_in').length > 0) {
      updateOptions('/sh/ajax/load_wall_port/', {
        'office_id': office_ports_id
      }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
    }
  } else {
    clearDependentFields(['#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
  }
}

function updateRackPortsOptions(rack_ports_id) {
  if (rack_ports_id) {
    if ($('#id_switch_ports').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'rack_id': rack_ports_id
      }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
    }
    if ($('#id_switch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_switch_port/', {
        'rack_id': rack_ports_id
      }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    }
    if ($('#id_patchera_ports').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'rack_id': rack_ports_id
      }, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));
    }
    if ($('#id_patch_port_in').length > 0) {
      updateOptions('/sh/ajax/load_patch_ports/', {
        'rack_id': rack_ports_id
      }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    }
  } else {
    clearDependentFields(['#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in']);
  }
}

function updateSwitchPortsOptions(switch_id) {
  updateOptions('/sh/ajax/load_switch_port/', {
    'switch_id': switch_id
  }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
}

function updatePatcheraPortsOptions(patchera_id) {
  updateOptions('/sh/ajax/load_patch_ports/', {
    'patchera_id': patchera_id
  }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
}


function updateBrandOptions(dev_type) {
  updateOptions('/sh/ajax/load_brand/', {
      'usage': 'device',
      'dev_type_name': dev_type
  }, $('select[name="brand"]'));
}

function updateModelOptions(dev_type, brand_id) {
  updateOptions('/sh/ajax/load_model/', {
      'usage': 'device',
      'dev_type_name': dev_type,
      'brand_id': brand_id
  }, $('select[name="dev_model"]'));
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