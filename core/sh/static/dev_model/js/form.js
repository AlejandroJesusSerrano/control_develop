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
