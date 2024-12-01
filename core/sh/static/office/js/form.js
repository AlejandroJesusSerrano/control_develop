$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#id_province').on('change', function(){
    clearDependentFields([
      '#id_location',
      '#id_edifice',
      '#id_dependency',
      '#id_loc'
    ]);
  });

  $('#id_location').on('change', function(){
    clearDependentFields([
      '#id_edifice',
      '#id_dependency',
      '#id_loc'
    ]);
  });

  $('#id_edifice').on('change', function(){
    clearDependentFields(['#id_loc']);
  });

  initializeFormSubmission('#myform', 'edit');

});


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