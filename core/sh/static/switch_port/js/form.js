// SELECT2 Initialization

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#toggle-switch-filters').on('click', function(e) {
    e.preventDefault();
    const filterLocCards = $('#filter-switch-cards')
    filterLocCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterLocCards.hasClass('d-none')) {
      $(this).html('Filtros para switch <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });
});
