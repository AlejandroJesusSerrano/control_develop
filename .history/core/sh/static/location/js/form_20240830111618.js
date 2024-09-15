// SHOW ERRORS IN FORM

function show_errors_in_form(errors){
  $('.is-invalid').removeClass('is-invalid');
  $('.invalid-feedback').remove();

  $.each(errors, function(field, fieldErrors) {
    let fieldElement = $(`[name="${field}"]`);

    if (fieldElement.length > 0) {
      fieldElement.addClass('is-invalid');
      let errorHtml = '<div class="invalid-feedback d-block">';

      $.each(fieldErrors, function(index, error){
        if (typeof error === 'object' && error.message) {
          errorHtml += error.message + '<br>';
        } else {
          errorHtml += error.message + '<br>';
        }
      });

      errorHtml += '</div>';
      fieldElement.after(errorHtml);
    }
  });
}
