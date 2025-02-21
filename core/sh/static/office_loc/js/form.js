$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  if ($('#id_location').length > 0) {
    $('select[name="location"]').on('change', function() {
        const location_id = $(this).val();
        if (!location_id) {
            console.warn('No se ha seleccionado una localidad válida en el formulario de Patchera.');
            clearDependentFields(['#id_edifice']);
            return;
        }
        console.log('Localidad seleccionada con ID:', location_id);
        updateOptions('/sh/ajax/load_edifices/', { 'location_id': location_id }, $('#id_edifice'));
    });
  }

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

  $('#edifice_add').on('click', function(e) {
    e.preventDefault();
    $('#edificeModal').modal('show');

    if ('{{action}}' === 'add') {
      var locationId = $('#id_location').val();
      var locationName = $('#id_location option:selected').text();

      if (locationId) {
        var newOption = new Option(locationName, locationId, true, true);
        $('#edificeModal').find('#id_location').append(newOption).trigger('change');
      }
    }
  });

  $('#edificeModal').on('click', '#location_add_from_edifice', function(e) {
    e.preventDefault();
    $('#locationModal').modal('show');
  });



  initializeFormSubmission('#myform', 'edit')

});

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