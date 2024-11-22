$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  updateBrandOptions();

  $('select[name="brand"]').on('change', function(){
    const brand_id = $(this).val();
    updateModelOptions(brand_id);
  });

  $('select[name="province"]').on('change', function(){
    const province_id = $(this).val();
    updateLocationOptions(province_id)
  })

  $('select[name="location"]').on('change', function(){
    const location_id = $(this).val();
    updateLocationRelatedOptions(location_id);
  });

  $('select[name="edifice"]').on('change', function(){
    const edifice_id = $(this).val();
    const dependency_id = $('select[name="dependency"]').val();
    updateOfficeOptions(edifice_id, dependency_id)
  });

  initializeFormSubmission('#myform', 'edit');

});

function updateBrandOptions(){
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
  },$('select[name="location"]'), $('#id_location').data('preselected'));
}


function updateLocationRelatedOptions(location_id) {
  if (location_id) {
    updateOptions('/sh/ajax/load_edifices/', {
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));

    updateOptions('/sh/ajax/load_dependency/', {
      'location_id': location_id,
    }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
  } else {
    $('select[name="edifice"], select[name="dependency"]').html('<option value="">----------</option>').trigger('change');
  }
}

function updateOfficeOptions(edifice_id, dependency_id) {
  updateOptions('/sh/ajax/load_office/', {
    'edifice_id': edifice_id,
    'dependency_id': dependency_id
  }, $('select[name="office"]'), $('#id_office').data('preselected'));
}

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/switch/list/';
    }, actionType)
  });
}
