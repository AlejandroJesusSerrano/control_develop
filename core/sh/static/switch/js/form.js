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

  if ($('#id_edifice_ports').length > 0) {
    $('select[name="edifice_ports"]').on('change', function(){
      const edifice_ports_id = $(this).val();
      updateEdificePortsOptions(edifice_ports_id);
    })
  }

  if ($('#id_loc_ports').length > 0) {
    $('select[name="loc_ports_id"]').on('change', function(){
      const loc_ports_id = $(this).val();
      updateLocPortsOptions(loc_ports_id);
    })
  }

  if ($('#id_office_ports').length > 0) {
    $('select[name="office_ports"]').on('change', function(){
      const office_ports_id = $(this).val();
      updateOfficePortsOptions(office_ports_id);
    })
  }

  if ($('#id_rack_ports').length > 0) {
    $('select[name="rack_ports"]').on('change', function(){
      const rack_ports_id = $(this).val();
      updateRackPortsOptions(rack_ports_id);
    })
  }

  if ($('#id_patchera_ports').length > 0) {
    $('select[name="patchera_ports"]').on('change', function(){
      const patchera_ports_id = $(this).val();
      updatePatcheraPortsOptions(patchera_ports_id);
    })
  }

  if ($('#id_switch_ports').length > 0) {
    $('select[name="switch_ports"]').on('change', function(){
      const switch_ports_id = $(this).val();
      updateSwitchPortsOptions(switch_ports_id);
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

function updateEdificePortsOptions(edifice_ports_id) {
  updateOptions('/sh/ajax/load_edifices/', {
    'edifice_ports_id': edifice_ports_id
  }, $('select[name="loc_ports_id"]'), $('#id_loc_ports').data('preselected'));
}

function updateLocPortsOptions(loc_ports_id) {
  updateOptions('/sh/ajax/load_loc/', {
    'loc_ports_id': loc_ports_id
  }, $('select[name="office_ports"]'), $('#id_office_ports').data('preselected'));
}

function updateOfficePortsOptions(office_ports_id) {
  updateOptions('/sh/ajax/load_rack/', {
    'office_ports_id': office_ports_id
  }, $('select[name="rack_ports"]'), $('#id_rack_ports').data('preselected'));

  updateOptions('/sh/ajax/load_switch/', {
    'office_ports_id': office_ports_id
  }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
}

function updateRackPortsOptions(rack_ports_id) {
  updateOptions('/sh/ajax/load_patchera/', {
    'rack_ports_id': rack_ports_id
  }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));

  updateOptions('/sh/ajax/load_patch_ports/', {
    'rack_ports_id': rack_ports_id
  }, $('select[name="patch_port"]'), $('#id_patch_port').data('preselected'));

  updateOptions('/sh/ajax/load_switch/', {
    'rack_ports_id': rack_ports_id
  }, $('select[name="switch"]'), $('#id_switch').data('preselected'));

  updateOptions('/sh/ajax/load_switch_port/', {
    'rack_ports_id': rack_ports_id
  }, $('select[name="switch_port"]'), $('#id_switch_port').data('preselected'));
}

function updatePatcheraPortsOptions(patchera_id) {
  updateOptions('/sh/ajax/load_patch_ports/', {
    'patchera_id': patchera_id
  }, $('select[name="patch_port"]'), $('#id_patch_port').data('preselected'));
}

function updateSwitchPortsOptions(switch_id) {
  updateOptions('/sh/ajax/load_switch_port/', {
    'switch_id': switch_id
  }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
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