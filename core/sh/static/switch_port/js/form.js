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

  $('#switch_popup_add').on('click', function() {
    let url = switchAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Switch', 'width=800,height=1080');
    popup.focus();
  });

  window.addEventListener('message', function(event) {
    if (event.data.type === 'switchAdded') {
        let switchId = event.data.id;
        let switchName = event.data.name;
        let select = $('#id_switch');
        let option = new Option(switchName, switchId, true, true);
        select.append(option).val(switchId).trigger('change');
    }
  });
});
