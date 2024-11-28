$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  $('#id_date_in').datepicker({
    format: 'dd/mm/yyyy',
    autoclose: true,
    todayHighlight: true,
    language: 'es'
  })

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
  }, $('select[name="model"]'), $('#id_model').data('preselected'));
}
