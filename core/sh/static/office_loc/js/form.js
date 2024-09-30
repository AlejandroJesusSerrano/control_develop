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
    updateEdificeOptions(location_id);
  });

  initializeFormSubmission('#myform', 'edit');

});

function updateLocationOptions(province_id){
  if (province_id) {
    updateOptions('/sh/ajax/search_office_loc_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
};

function updateEdificeOptions(location_id) {
  if (location_id) {
    updateOptions('/sh/ajax/search_office_loc_edifice/', {
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data ('preselected'));
  }
};

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefautlt();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/office_loc/list';
    }, actionType)
  });
}