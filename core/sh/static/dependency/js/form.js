$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#toggle-office-filters').on('click', function (e) {
    e.preventDefault();
    const filterLocCards = $('#filter-office-cards')
    filterLocCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterLocCards.hasClass('d-none')) {
      $(this).html('Filtros de Localidades <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });

  $('select[name="province"]').on('change', function(){
    const province_id = $(this).val();
    updateLocationOptions(province_id);
  });

  initializeFormSubmission('#dependencyForm', 'edit');

});

function updateLocationOptions(province_id) {
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', {
      'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
};

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/dependency/list';
    }, actionType)
  });
}