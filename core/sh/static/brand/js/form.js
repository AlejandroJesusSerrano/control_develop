// SHOW ERRORS IN FORM

function show_errors_in_form(errors){

  $('.is-invalid').removeClass('is-invalid');
  $('.invalid-feedback').remove();

  $.each(errors, function(field, fieldErrors) {
    let fieldElement = $(`[name="${field}"]`);
    console.log("Field Element: ", fieldElement)

    if (fieldElement.length > 0) {
      fieldElement.addClass('is-invalid');
      let errorHtml = '<div class="invalid-feedback d-block">';

      $.each(fieldErrors, function(index, error){
        errorHtml += error.message + '<br>';
      });

      errorHtml += '</div>';
      fieldElement.after(errorHtml);

    }
  });
}