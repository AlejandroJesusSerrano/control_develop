/// SELECT 2

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });
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

function updateLocationOptions(province_id) {
  if (province_id) {
    updateOptions('/your-url-to-get-locations/', {  // Asegúrate de que esta URL sea correcta
      'action': 'search_location',
      'province_id': province_id,
      'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()  // Incluye el token CSRF
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  } else {
    // Limpiar el campo `location` y reinicializar select2
    $('select[name="location"]').html('<option value="">----------</option>').trigger('change').select2({
      theme: 'bootstrap'
    });

    // Limpiar también el campo `edifice` ya que depende de `location`
    $('select[name="edifice"]').html('<option value="">----------</option>').trigger('change').select2({
      theme: 'bootstrap'
    });
  }
};

// function updateLocationOptions(province_id) {
//   if (province_id) {
//     updateOptions(window.location.pathname, {
//     'action': 'search_location',
//     'province_id': province_id,
//     }, $('select[name="location"]'), $('#id_location').data('preselected'));
//   } else {
//     $('select[name="location"]').html('<option value="">----------</option>');
//   }
// };

function updateEdificeOptions(location_id) {
  if (location_id) {
    updateOptions(window.location.pathname, {
    'action': 'search_edifice',
    'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  } else {
    $('select[name="edifice"]').html('<option value="">----------</option>');
  }
};

// UPDATE OPTIONS

function updateOptions(url, data, selectElement, preselectedValue) {
  let options = '<option value="">----------</option>';

  $.ajax({
    url: url,
    type: 'POST',
    data: data,
    dataType: 'json'
  }).done(function (data) {

    if (typeof data === 'object' && !data.hasOwnProperty('error')) {
      $.each(data, function (key, value) {
        options += '<option value="' + value.id + '">' + value.name + '</option>';
      });
      selectElement.html(options);

      selectElement.select2({
        theme: 'bootstrap'
      });

      if (preselectedValue) {
        selectElement.val(preselectedValue).trigger('change');
      } else {
        selectElement.trigger('change');
      }

    } else if(data.hasOwnProperty('error')) {
      message_error(data.error);

    } else {
      message_error('Ha ocurrido un error inesperado');
    }

  }).fail(function (jqXHR, textStatus, errorThrown) {
    message_error(textStatus + ': ' + errorThrown);
  });
};

// INITALIZE SELECTS

function initializeSelects() {
  const province_id = $('select[name="province"]').val();
  const location_id = $('select[name="location"]').val();

  if (province_id) {
    updateLocationOptions(province_id);
  }

  if (location_id) {
    updateEdificeOptions(location_id);
  }

}

// START

$(document).ready(function() {
  initializeSelects();

  $('select[name="province"]').on('change', function(){
    updateLocationOptions($(this).val());
  });

  $('select[name="location"]').on('change', function(){
    updateEdificeOptions($(this).val());
  });

});