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

  $('#office_popup_add').on('click', function() {
    let url = officeAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar oficina', 'width=800, height=800');
    popup.focus();
  });

  $('#switch_port_popup_add').on('click', function() {
    let url = switchPortAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar puerto de switch', 'width=800, height=700');
    popup.focus();
  });

  $('#patch_port_popup_add').on('click', function() {
    let url = patchPortAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar puerto de patchera', 'width=800, height=400');
    popup.focus();
  });

  window.addEventListener('message', function(event) {
    if (event.data.type === 'officeAdded') {
      let officeId = event.data.id;
      let brandName = event.data.brand.name;
      let select = $('#id_office');
      let option = new Option(brandName, officeId, true, true);
      select.append(option).trigger('change');
    }

    if (event.data.type === 'switch_portAdded') {
      let switch_portId = event.data.id;
      let switch_portName = event.data.name;
      let select = $('#id_switch_port_in');
      let option = new Option(switch_portName, switch_portId, true, true);
      select.append(option).trigger('change');
    }

    if (event.data.type === 'patch_portAdded') {
      let patch_portId = event.data.id;
      let patch_portName = event.data.name;
      let select = $('#id_patch_port_in');
      let option = new Option(patch_portName, patch_portId, true, true);
      select.append(option).trigger('change');
    }
  });S

  initializeFormSubmission('#myform', 'edit');

});




function updateEdificePortsOptions(edifice_port_id) {
  if (edifice_port_id) {
    if ($('#id_loc_port').length > 0) {
      updateOptions('/sh/ajax/load_loc/', {
        'edifice_id': edifice_port_id
      }, $('select[name="loc_port"]'), $('#id_loc_port').data('preselected'));
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
  }
}


function updateRackPortsOptions(rack_port_id) {
  if (rack_port_id){
    if ($('#id_patchera_port').length > 0) {
      updateOptions('/sh/ajax/load_patchera/', {
        'rack_id': rack_port_id
      }, $('select[name="patchera_port"]'), $('#id_patchera_port').data('preselected'));
    }

    if ($('#id_switch').length > 0) {
      updateOptions('/sh/ajax/load_switch/', {
        'rack_id': rack_port_id
      }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
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
