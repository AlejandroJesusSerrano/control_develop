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

  // Abrir modal de edificio
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

      var provinceId = $('#id_province').val();
      var provinceName = $('#id_province option:selected').text();

      if (provinceId) {
        var newOption = new Option(provinceName, provinceId, true, true);
        $('#edificeModal').find('#id_province').append(newOption).trigger('change');
      }
    }
  });

  // Abir modal de localidad desde modal de edificio
  $('#edificeModal').on('click', '#location_add_from_edifice', function(e) {
    e.preventDefault();
    $('#locationModal').modal('show');
  });

  // Abrir modal de provincia desde modal de localidad
  $('#locationModal').on('click', '#province_add_from_location', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
  });

  // enviar formulario de edificio (AJAX)
  $('#edificeForm').on('submit', function(e) {
    e.preventDefault();
    var form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
      console.log('Respuesta AJAX: ', response);
      $('#edificeModal').modal('hide');

      var newOption = new Option(response.edifice_name, response.edifice_id, true, true);
      $('#id_edifice').append(newOption).trigger('change')

      form.reset();
    }, 'add');
  });

  // enviar formulario de localidad (AJAX)
  $('#locationForm').on('submit', function(e) {
    e.preventDefault();
    var form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

      $('#locationModal').modal('hide');

      var newOption = new Option(response.location_name, response.location_id, true, true);
      $('#edificeModal').find('#id_location').append(newOption).trigger('change');

      form.reset();
    }, 'add');
  });

  // enviar formulario de provincia (AJAX)
  $('#provinceForm').on('submit', function(e) {
    e.preventDefault();
    var form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

      $('#provinceModal').modal('hide');

      var newOption = new Option(response.province_name, response.province_id, true, true);
      $('#locationModal').find('#id_province').append(newOption).trigger('change');

      form.reset();
    }, 'add');
  });

  if ('{{action}}' === 'edit') {
    var edificeId = $('#id_edifice').val();
    var edificeName = $('#id_edifice option:selected').text();

    if (edificeId) {
        var newOption = new Option(edificeName, edificeId, true, true);
        $('#id_edifice').append(newOption).trigger('change');
    }
  }


  initializeFormSubmission('#myform', 'edit')

});

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/office_loc/list';
    }, actionType)
  });
}
