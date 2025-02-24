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

  $('#dev_type_add').on('click', function(e) {
    e.preventDefault();
    $('#devTypeModal').modal('show');
  });

  $('#brand_add').on('click', function(e) {
    e.preventDefault();
    $('#brandModal').modal('show');
  });

  $('#devTypeForm').on('submit', function(e) {
    e.preventDefault();
    let form = $(this);
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
      $('#devTypeModal').modal('hide');

      let newOption = new Option(response.dev_type_name, response.dev_type_id, true, true);
      $('#id_dev_type').append(newOption).trigger('cahnge');

      form.reset();
    }, 'add');

  });

  $('#brandForm').on('submit', function(e) {
    e.preventDefault();
    let form = $(this);
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
      $('#brandModal').modal('hide');

      let newOption = new Option(response.brand_name, response.brand_id, true, true);
      $('#id_brand').append(newOption).trigger('cahnge');

      form.reset();
    }, 'add');

  });

  if ('{{action}}' === 'edit') {
    
    $('#devTypeForm').on('submit', function(e) {
      e.preventDefault();
      let form = $(this);
      submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
        $('#devTypeModal').modal('hide');

        let newOption = new Option(response.dev_type_name, response.dev_type_id, true, true);
        $('#id_dev_type').append(newOption).trigger('cahnge');

        form.reset();
      }, 'update');

    });

    $('#brandForm').on('submit', function(e) {
      e.preventDefault();
      let form = $(this);
      submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
        $('#brandModal').modal('hide');

        let newOption = new Option(response.brand_name, response.brand_id, true, true);
        $('#id_brand').append(newOption).trigger('cahnge');

        form.reset();
      }, 'update');

    });
  }

});
