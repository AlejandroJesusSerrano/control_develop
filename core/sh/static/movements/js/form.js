$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  $('#id_suply_date_in_button').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true,
    language: 'es',
    container: 'body',
    orientation: 'auto',
    zindex_offset: 1050
  }).on('changeDate', function(e) {
    $('#id_suply_date_in_input').val(e.format('dd/mm/yyyy'));
  });

  // $('#id_suply_date_in_input').datepicker({
  //   format: 'dd/mm/yyyy',
  //   autoclose: true,
  //   todayHighlight: true,
  //   language: 'es'
  // })

  updateBrandOptions();

  $('select[name="brand"]').on('change', function() {
    const brand_id = $(this).val();
    updateModelOptions(brand_id);
  });

  initializeFormSubmission('#myform', 'edit');
});

// Funciones de actualización
function updateBrandOptions() {
  const dev_type_name = 'IMPRESORA';
  updateOptions('/sh/ajax/load_brand/', {
    'dev_type_name': dev_type_name
  }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
}

function updateModelOptions(brand_id) {
  const dev_type_name = 'IMPRESORA';
  updateOptions('/sh/ajax/load_model/', {
    'brand_id': brand_id,
    'dev_type_name': dev_type_name
  }, $('select[name="dev_model"]'), $('#id_dev_model').data('preselected'));
}
