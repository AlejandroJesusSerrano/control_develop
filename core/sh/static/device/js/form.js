// SELECT 2

$(document).ready(function() { 
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('select[name="province"]').on('change', function(){
    const province_id = $(this).val();
    updateLocationOptions(province_id);
  });

  $('select[name="location"]').on('change', function(){
    const location_id = $(this).val();
    updateLocationsreferredOptions(location_id);
  });

  $('select[name="edifice"]').on('change', function(){
    const edifice_id = $(this).val();
    updateWingFloorOptions(edifice_id);
  })

  $('select[name="loc"]').on('change', function(){
    const loc_id = $(this).val();
    updateOfficeOptions(loc_id)
  })

  $('select[name="office"]').on('change', function(){
    const office_id = $(this).val();
    updateOfficeRelatedOptions(office_id)
  })

  $('select[name="brand"], select[name="dev_type"]').on('change', function(){
    const brand_id = $('select[name="brand"]').val();
    const dev_type_id = $('select[name="dev_type"]').val();
    updateModelsOptions(brand_id, dev_type_id)
  })

  initializeFormSubmission('#myform', 'edit');
});

function updateLocationOptions(province_id){
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
};

function updateLocationsreferredOptions(location_id) {
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

function updateWingFloorOptions(edifice_id) {
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
}

function updateOfficeRelatedOptions(office_id) {
  if (office_id) {
    updateOptions('/sh/ajax/load_wall_port/',
      {'office_id': office_id},
      $('select[name="wall_port"]'),
      $('#id_wall_port').data('preselected'),
    );
    updateOptions('/sh/ajax/load_switch_port/',
      {'office_id': office_id},
      $('select[name="switch_port"]'),
      $('#id_switch_port').data('preselected'),
    );
    updateOptions('/sh/ajax/load_employee/',
      {'office_id': office_id},
      $('select[name="employee"]'),
      $('#id_employee').data('preselected'),
    );
  }
}

function updateModelsOptions(brand_id, dev_type_id) {
  if (brand_id && dev_type_id) {
    updateOptions('/sh/ajax/load_model/',
      {
        'brand_id': brand_id,
        'dev_type_id':dev_type_id
      },
      $('select[name="dev_model"]'),
      $('#id_dev_model').data('preselected')
    )
  }
}

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/office/list';
    }, actionType)
  });
}