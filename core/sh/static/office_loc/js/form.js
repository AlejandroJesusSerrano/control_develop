$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#toggle-edifice-filters').on('click', function (e) {
    e.preventDefault();
    const filterEdifCards = $('#filter-edifice-cards')
    filterEdifCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterEdifCards.hasClass('d-none')) {
      $(this).html('Filtros de Edificios <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });

  $('select[name="province"]').on('change', function(){
    const province_id = $(this).val();
    updateProvinceOptions(province_id);
  });

  $('select[name="location"]').on('change', function(){
    const location_id = $(this).val();
    updateEdificeOptions(location_id)
  })

  initializeFormSubmission('#myform', 'edit')

});

function updateProvinceOptions(province_id) {
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));

    updateOptions('/sh/ajax/load_edifices/', {
      'province_id': province_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  } else {
    clearDependentFields(['#id_location', '#id_edifice'])
  };
}

function updateLocationOptions(location_id) {
  if (location_id) {
    updateOptions('/sh/ajax/load_edifices/', {
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  }
}

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefautlt();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/office_loc/list';
    }, actionType)
  });
}