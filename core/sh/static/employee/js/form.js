$(document).ready(function() {
  $('.select2').select2({
    theme: 'bootstrap',
  });

  $('#custom_avatar_button').on('click', function() {
    $('#id_avatar_image_input').click();
  });

  $('#id_avatar_image_input').on('change', function() {
    const fileName = $(this).val().split('//').pop();
    $('#file_name').text(fileName || 'Ningún archivo seleccionado');
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

  initializeFormSubmission('#myform', 'edit');

});

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/switch/list';
    }, actionType);
  });
}