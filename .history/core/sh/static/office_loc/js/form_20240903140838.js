// SELECT 2

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  initializeSelects();
});

// SHOW ERRORS IN FORM

function show_errors_in_form(errors){
  $('.is-invalid').removeClass('is-invalid');
  $('.invalid-feedback').remove();

  $.each(errors, function(field, fieldErrors) {
    let fieldElement = $(`[name="${field}"]`);

    if (fieldElement.length > 0) {
      fieldElement.addClass('is-invalid');
      let errorHtml = '<div class="invalid-feedback d-block">';

      $.each(fieldErrors, function(index, error){
        if (typeof error === 'object' && error.message) {
          errorHtml += error.message + '<br>';
        } else {
          errorHtml += error.message + '<br>';
        }
      });

      errorHtml += '</div>';
      fieldElement.after(errorHtml);
    }
  });
}

// UPDATE LOCATION & EDIFICE OPTIONS

function updateLocationsOptions(provinceId) {
  if (provinceId) {
    updateOptions(window.location.pathname, {
      'action': 'search_location',
      'province_Id': provinceId,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  } else {
    $('select[name="location"]').html('<option value="">----------</option>').trigger('change');
    $('select[name="edifice"]').html('<option value="">----------</option>').trigger('change');
  }
}

function updateEdificeOptions(locationId) {
  if (locationId) {
    updateOptions(window.location.pathname, {
      'action': 'search_edifice',
      'location_id': locationId,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  } else {
    $('select[name="edifice"]').html('<option value="">----------</option>');
  }
}

// UPDATE OPTIONS

function updateOptions(url, data, selectElement, preselectedValue){
  let options = '<option value="">----------</option>';

  $.ajax({
    url:url,
    type: 'POST',
    data: data,
    dataType: 'json'
  }).done(function (data) {
    if (typeof data === 'object' && !data.hasOwnProperty('error')) {
      $.each(data, function (index, value) {
        options += '<option value="' + value.id + '">' + value.name + '</option>';
      });
      selectElement.html(options).trigger('change');

      selectElement.select2({
        theme: 'bootstrap'
      });

      if (preselectedValue) {
        selectElement.val(preselectedValue).trigger('change');
      }

    } else if (data.hasOwnProperty('error')) {

      message_error(data.error);

    } else {
      message_error('Ha ocurrido un error inesperado');
    }

  }).fail(function (jqXHR, textStatus, errorThrown) {
    message_error(textStatus + ': ' + errorThrown);
  });
};

// INITIALIZE SELECTS

function initializeSelects() {
  $('select[name="province"]').on('change', function (){
    const provinceId = $(this).val();
    updateLocationsOptions(provinceId);
    $('select[name="edifice"]').html('<option value="">----------</option>').trigger('change');
  });

  $('select[name="location"]').on('change', function () {
    const locationId = $(this).val();
    updateEdificeOptions(locationId);
  });
}