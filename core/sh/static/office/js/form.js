$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  if ($('#id_location').length > 0) {
    $('select[name="location"]').on('change', function() {
        const location_id = $(this).val();
        if (!location_id) {
            console.warn('No se ha seleccionado una localidad válida en el formulario de Patchera.');
            clearDependentFields(['#id_edifice', '#id_loc', '#id_office', '#id_rack_patchera']); // Limpia los campos dependientes
            return;
        }
        console.log('Localidad seleccionada con ID:', location_id);
        updateOptions('/sh/ajax/load_edifices/', { 'location_id': location_id }, $('#id_edifice'));
    });
  }

  $('#toggle-office-filters').on('click', function (e) {
    e.preventDefault();
    const filterLocCards = $('#filter-office-cards')
    filterLocCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterLocCards.hasClass('d-none')) {
      $(this).html('Filtros para Edificio, Dependencia y Ubicación <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });

  initializeFormSubmission('#myform', 'edit');

});

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/wall_port/list/';
    }, actionType);
  });
}

