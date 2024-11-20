$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('select[name="rack"]').on('change', function(){
    const rack_id = $(this).val();
    updateRackOptions(rack_id);
  });

  initializeFormSubmission('#myform', 'edit');
});

function updateRackOptions(rack_id){
  if (rack_id) {
    updateOptions('/sh/ajax/load_patchera/', {
      'rack_id': rack_id,
    }, $('select[name="patch"]'), $('#id_patch').data('preselected'));
  }
};

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/patch_port/list';
    }, actionType)
  });
}