// SELECT 2

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('.select2').on('select2:open', function() {
    $('.select2-container').addClass('bg-dark text-light');
    $('.select2-results').addClass('bg-dark text-light');
  });

  $('#province_add').click(function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');

    $.ajax({
      url: '/sh/prov/add/',
      type: 'GET',
      success: function(data) {
        $('#provinceModalContent').html(data);
      },
      error: function(xhr, status, error) {
        console.log('Error al cargar el formulario: ' + error);
      }
    });
  });

  $('#provinceModal').on('submit', '#provinceForm', function(e) {
    e.preventDefault();
    let form = $(this);

    $.ajax({
      url: form.attr('action'),
      type: form.attr('method'),
      data: form.serialize(),
      success: function(data) {
        if (data.success) {
          let newOption = new Option(data.new_province.name, data.new_province.id, true, true);
          $('[name="provice"]').append(newOption).trigger('change');
          $('#provinceModal').modal('hide');
        } else {
          $('#provinceModalContent').html(data.html_form);
        }
      },
      error: function(xhr, status, error) {
        console.log('Error al guardar la provincia: ' + error);
      }
    });
  });
});

