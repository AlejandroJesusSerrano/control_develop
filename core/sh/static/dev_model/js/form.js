function show_errors_in_form(errors){
  $('.is-invalid').removeClass('is-invalid');
  $('.invalid-feedback').remove();

  $.each(errors, function(field, fieldErrors) {
    let fieldElement = $(`[name="${field}"]`);

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

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#custom_file_button').click(function() {
    $('#id_image_selector').click();
  });

  $('#id_image_selector').change(function() {
    const fileName = $(this).val().split('\\').pop();
    $('#file_name').text(fileName || 'Ningún archivo seleccionado');
  });
});
