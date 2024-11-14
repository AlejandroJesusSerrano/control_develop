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