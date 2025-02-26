$(document).ready(function() {

  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#id_location').select2({
    theme: 'bootstrap'
  });

  $('#id_edifice').select2({
    theme: 'bootstrap'
  });

  if ($('#id_location').length > 0) {
    $('select[name="location"]').on('change', function() {
        const location_id = $(this).val();
        if (!location_id) {
            console.warn('No se ha seleccionado una localidad válida en el formulario de Oficina.');
            clearDependentFields(['#id_edifice', '#id_loc', '#id_dependency']);
            return;
        }
        console.log('Localidad seleccionada con ID:', location_id);
        updateOptions('/sh/ajax/load_office/', { 'location_id': location_id }, $('#id_edifice'));
    });
  }

  $('#location_add').on('click', function(e) {
    e.preventDefault();
    $('#locationModal').modal('show');

    if ('{{action}}' === 'add') {
      let provinceId = $('#id_province').val();
      let provinceName = $('#id_province option:selected').text();

      if (provinceId) {
        let newOption = new Option(provinceName, provinceId, true, true);
        $('#locationModal').find('#id_province').append(newOption).trigger('change');
      }
    }
  });

  // Abrir modal de dependencia
  $('#dependency_add').on('click', function(e) {
    e.preventDefault();
    $('#dependencyModal').modal('show');

    if ('{{action}}' === 'add') {
      let locationId = $('#id_location_main').val();
      let locationName = $('#id_location_main option:selected').text();

      if (locationId) {
        let newOption = new Option(locationName, locationId, true, true);
        $('#dependencyModal').find('#id_location_main').append(newOption).trigger('change');
      }

      let provinceId = $('#id_province_main').val();
      let provinceName = $('#id_province_main option:selected').text();

      if (provinceId) {
        let newOption = new Option(provinceName, provinceId, true, true);
        $('#dependencyModal').find('#id_province_main').append(newOption).trigger('change');
      }
    }
  });

  // Abrir modal de edificio
  $('#edifice_add').on('click', function(e) {
    e.preventDefault();
    $('#edificeModal').modal('show');

    if ('{{action}}' === 'add') {
      let locationId = $('#id_location_main').val();
      let locationName = $('#id_location_main option:selected').text();

      if (locationId) {
        let newOption = new Option(locationName, locationId, true, true);
        $('#edificeModal').find('#id_location_main').append(newOption).trigger('change');
      }

      let provinceId = $('#id_province_main').val();
      let provinceName = $('#id_province_main option:selected').text();

      if (provinceId) {
        let newOption = new Option(provinceName, provinceId, true, true);
        $('#edificeModal').find('#id_province_main').append(newOption).trigger('change');
      }
    }
  });

  // Abrir modal de ubicación de oficina
  $('#loc_add').on('click', function(e) {
    e.preventDefault();
    $('#locModal').modal('show')

    if ('{{action}}' === 'add') {
      let edificeId = $('#id_edifice_main').val();
      let edificeName = $('#id_edifice_main option:selected').text();


      if (edificeId) {
        let newOption = new Option(edificeName, edificeId, true, true);
        $('#locModal').find('#id_edifice_main').append(newOption).trigger('change');
      }

      let locationId = $('#id_location_main').val();
      let locationName = $('#id_location_main option:selected').text();

      if (locationId) {
        let newOption = new Option(locationName, locationId, true, true);
        $('#locModal').find('#id_location_main').append(newOption).trigger('change');
      }

      let provinceId = $('#id_province_main').val();
      let provinceName = $('#id_province_main option:selected').text();

      if (provinceId) {
        let newOption = new Option(provinceName, provinceId, true, true);
        $('#locModal').find('#id_province_main').append(newOption).trigger('change');
      }
    }
  });


  // Abrir modal de provincia desde modal de localidad
  $('#locationModal').on('click', '#province_add_from_location', function(e) {
    e.preventDefault();
    $('#provinceModal').modal('show');
  });


  $('#locationForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

      $('#locationModal').modal('hide');

      let newOption = new Option(response.location_name, response.location_id, true, true);
      $('#id_location').append(newOption).trigger('change');

      form.reset();
    }, 'add');
  });


  $('#dependencyForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
      console.log('Respuesta AJAX: ', response);
      $('#dependencyModal').modal('hide');

      let newOption = new Option(response.dependency_name, response.dependency_id, true, true);
      $('#id_dependency_main').append(newOption).trigger('change')

      form.reset();
    }, 'add');
  });


  $('#edificeForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
      console.log('Respuesta AJAX: ', response);
      $('#edificeModal').modal('hide');

      let newOption = new Option(response.edifice_name, response.edifice_id, true, true);
      $('#id_edifice_main').append(newOption).trigger('change')

      form.reset();
    }, 'add');
  });


  $('#locForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {
      console.log('Respuesta AJAX: ', response);
      $('#locModal').modal('hide');

      let newOption = new Option(response.loc_name, response.loc_id, true, true);
      $('#id_loc').append(newOption).trigger('change')

      form.reset();
    }, 'add');
  });


  $('#provinceForm').on('submit', function(e) {
    e.preventDefault();
    let form = this;
    submit_with_ajax($(this).attr('action'), new FormData(form), function(response) {

      $('#provinceModal').modal('hide');

      let newOption = new Option(response.province_name, response.province_id, true, true);
      $('#locationModal').find('#id_province').append(newOption).trigger('change');

      form.reset();
    }, 'add');
  });

  if ('{{action}}' === 'edit') {
    let edificeId = $('#id_edifice').val();
    let edificeName = $('#id_edifice option:selected').text();
    let depdendecyId = $('#id_dependency').val();
    let depdendecyName = $('#id_dependency option:selected').text();

    if (edificeId) {
        let newOption = new Option(edificeName, edificeId, true, true);
        $('#id_edifice').append(newOption).trigger('change');
    }

    if (depdendecyId) {
        let newOption = new Option(depdendecyName, depdendecyId, true, true);
        $('#id_dependency').append(newOption).trigger('change');
    }
  }

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

