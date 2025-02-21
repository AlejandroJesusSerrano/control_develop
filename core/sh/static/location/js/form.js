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

    var parameters = new FormData(this);
    var actionUrl = $(this).attr('action');

    submit_with_ajax(actionUrl, parameters, function() {
      location.reload();
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

