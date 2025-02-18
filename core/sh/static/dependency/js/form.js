$(document).ready(function() {

  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#location_add').on('click', function(e) {
    e.preventDefault();
    $('#locationModal').modal('show');
  });

  $('#locationModal form').on('submit', function(e) {
    e.preventDefault();

    var parameters = new FormData(this);
    var actionUrl = $(this).attr('action');

    submit_with_ajax(actionUrl, parameters, function() {
      location.reload();
    });
  });

  $('#province_add').on('click', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
  });

  initializeFormSubmission('#dependencyForm', 'edit');

});

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/dependency/list';
    }, actionType)
  });
}