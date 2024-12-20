$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  $('#toggle-office-filters').on('click', function (e) {
    e.preventDefault();

    const filterLocCards = $('#filter-office-cards')

    filterLocCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterLocCards.hasClass('d-none')) {
      $(this).html('Filtros de oficinas <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });
});