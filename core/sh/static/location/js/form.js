// SELECT 2

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('.select2').on('select2:open', function() {
    $('.select2-container').addClass('bg-dark text-light');
    $('.select2-results').addClass('bg-dark text-light');
  });

  $('#province_add').on('click', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
  });

  $('#provinceModal form').on('submit', function(e) {
    e.preventDefault();

    let form = this;

    submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {
      $('#provinceModal').modal('hide');

      let newOption = new Option(response.province_name, response.province_id, true, true);
      $('#id_province').append(newOption).trigger('change');

      form.reset();
    }, 'add');
  });

  if ('{{action}}' === 'edit') {
    var provinceId = $('#id_province').val();
    var ProvinceName = $('#id_province option:selected').text();

    if (provinceId) {
        var newOption = new Option(ProvinceName, provinceId, true, true);
        $('#id_location').append(newOption).trigger('change');
    }
  }
});

