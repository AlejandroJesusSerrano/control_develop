// SELECT 2

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#province_add').on('click', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
  });

  $('#provinceForm').on('submit', function(e) {
    e.preventDefault();
    var form = this;
    submit_with_ajax($(form).attr('action'), new FormData(form), function(response) {

        $('#provinceModal').modal('hide');

        var newOption = new Option(response.location_name, response.location_id, true, true);
        $('#id_province').append(newOption).trigger('change');

        form.reset();
    },'add');

});

  if ('{{action}}' === 'edit') {
    var provinceId = $('#id_province').val();
    var provinceName = $('#id_province option:selected').text();

    if (provinceId) {
        var newOption = new Option(provinceName, provinceId, true, true);
        $('#id_location').append(newOption).trigger('change');
    }
  }
});

