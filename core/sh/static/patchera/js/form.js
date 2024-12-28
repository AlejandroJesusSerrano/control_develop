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
})

$('#toggle-rack-filters').on('click', function (e) {
  e.preventDefault();
  const filterLocCards = $('#filter-rack-cards')
  filterLocCards.toggleClass('d-none')

  $(this).toggleClass('active btn-primary btn-secondary')

  if (filterLocCards.hasClass('d-none')) {
    $(this).html('Filtrar Rack <i class="fas fa-search"></i>');
  } else {
    $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
  }
});
