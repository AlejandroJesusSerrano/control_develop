// SELECT2 Initialization

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  // Eventos para campos dependientes

  // Cuando cambia la provincia
  $('select[name="province"]').on('change', function(){
    const province_id = $(this).val();
    updateLocationOptions(province_id);
  });

  // Cuando cambia la localidad
  $('select[name="location"]').on('change', function(){
    const location_id = $(this).val();
    updateDependencyAndEdificeOptions(location_id);
  });

  // Cuando cambia el edificio
  $('select[name="edifice"]').on('change', function(){
    const edifice_id = $(this).val();
    updateLocOptions(edifice_id);
  });

  // Cuando cambia la ubicación
  $('select[name="loc"]').on('change', function(){
    const loc_id = $(this).val();
    updateOfficeOptions(loc_id);
  });

  // Cuando cambia la oficina
  $('select[name="office"]').on('change', function(){
    const office_id = $(this).val();
    updateRackAndSwitchOptions(office_id);
  });

  // Cuando cambian la marca o el tipo de dispositivo
  $('select[name="brand"], select[name="dev_type"]').on('change', function(){
    const brand_id = $('select[name="brand"]').val();
    const dev_type_id = $('select[name="dev_type"]').val();
    updateDevModelOptions(brand_id, dev_type_id);
  });

  // Cuando cambia el rack
  $('select[name="rack"]').on('change', function(){
    const rack_id = $(this).val();
    updatePatcheraOptions(rack_id);
  });

  // Cuando cambia la patchera
  $('select[name="patchera"]').on('change', function(){
    const patchera_id = $(this).val();
    updatePatchPortsOptions(patchera_id);
  });

  // Inicializar el envío del formulario
  initializeFormSubmission('#switch_portForm', 'edit');
});

// Funciones para actualizar opciones

function updateLocationOptions(province_id){
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
};

function updateDependencyAndEdificeOptions(location_id) {
  if (location_id) {
    updateOptions(
      '/sh/ajax/load_dependency/',
      {'location_id': location_id},
      $('select[name="dependency"]'),
      $('#id_dependency').data('preselected'),
    );
    updateOptions(
      '/sh/ajax/load_edifices/',
      {'location_id': location_id},
      $('select[name="edifice"]'),
      $('#id_edifice').data('preselected'),
    );
  }
};

function updateLocOptions(edifice_id) {
  if (edifice_id) {
    updateOptions('/sh/ajax/load_loc/', {
      'edifice_id': edifice_id,
    }, $('select[name="loc"]'), $('#id_loc').data('preselected'));
  }
};

function updateOfficeOptions(loc_id) {
  if (loc_id) {
    updateOptions('/sh/ajax/load_office/', {
      'loc_id': loc_id
    }, $('select[name="office"]'), $('#id_office').data('preselected'));
  }
};

function updateRackAndSwitchOptions(office_id) {
  if (office_id) {
    updateOptions('/sh/ajax/load_rack/', {
      'office_id': office_id
    }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
    updateOptions('/sh/ajax/load_switch/', {
      'office_id': office_id
    }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
  }
};

function updateDevModelOptions(brand_id, dev_type_id) {
  if (brand_id || dev_type_id) {
    updateOptions('/sh/ajax/load_model/', {
      'brand_id': brand_id,
      'dev_type_id': dev_type_id
    }, $('select[name="dev_model"]'), $('#id_dev_model').data('preselected'));
  } else {
    $('select[name="dev_model"]').empty();
  }
};

function updatePatcheraOptions(rack_id) {
  if (rack_id) {
    updateOptions('/sh/ajax/load_patchera/', {
      'rack_id': rack_id
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
  }
};

function updatePatchPortsOptions(patchera_id) {
  if (patchera_id) {
    updateOptions('/sh/ajax/load_patch_ports/', {
      'patchera_id': patchera_id
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    updateOptions('/sh/ajax/load_patch_ports/', {
      'patchera_id': patchera_id
    }, $('select[name="patch_port_out"]'), $('#id_patch_port_out').data('preselected'));
  }
};
