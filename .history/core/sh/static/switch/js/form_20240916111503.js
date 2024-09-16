// SELECT 2

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

// UPDATE OPTIONS

function updateOptions(url, data, selectElement, preselectedValue) {
  let options = '<option value="">----------</option>';

  console.log("Enviando datos a:", url);
  console.log("Datos enviados:", data);

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
      selectElement.html(options).trigger('change');

      selectElement.select2({
        theme: 'bootstrap'
      });

      if (preselectedValue) {
        selectElement.val(preselectedValue).trigger('change');
      }

    } else if(data.hasOwnProperty('error')) {
      message_error(data.error);

    } else {
      message_error('Ha ocurrido un error inesperado');
    }

  }).fail(function (jqXHR, textStatus, errorThrown) {
    console.log("Error en la solicitud AJAX:", jqXHR.responseText);
    message_error(textStatus + ': ' + errorThrown);
  });
};

// INITALIZE SELECTS

function initializeSelects() {
  const brand_id = $('select[name="brand"]').val();
  const location_id = $('select[name="location"]').val();
  const dependency_id = $('select[name="dependency"]').val();
  const edifice_id = $('select[name="edifice"]').val();

  if (brand_id) {
    updateModelOptions(brand_id)
  }

  if (location_id) {
    updateLocationRelatedOptions(location_id);
  }

  if (edifice_id && dependency_id) {
    updateOfficeLocationOptions(edifice_id, dependency_id)
  }


}

// UPDATE OPTIONS

function updateModelOptions(brand_id) {
  const dev_type_name = 'SWITCH'
  updateOptions('/ajax/search_model/', {
    'brand_id': brand_id,
    'dev_type_name': dev_type_name
  }, $('select[name="model"]'), $('#id_model').data('preselected'));
};

function updateLocationrelatedOptions(location_id) {
  if (location_id) {
    updateOptions('/ajax/search_edifice/', {
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));

    updateOptions('/ajax/search_dependency', {
      'location_id': location_id,
    }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
  } else {
    $('select[name="edifice"], select[name="dependency"]').html('<option value="">----------</option>').trigger('change');
  };
};

function updateOfficeOptions(edifice_id, dependency_id) {
    updateOptions('/ajax/search_office/', {
      'edifice_id': edifice_id,
      'dependency_id': dependency_id
    }, $('select[name="office"]'), $('#id_office').data('preselected'));
};

// START

$(document).ready(function() {
  initializeSelects();

  $('select[name="brand"]').on('change', function(){
    updateModelOptions($(this).val());
  });

  $('select[name="location"]').on('change', function(){
    updateLocationRelatedOptions($(this).val());
  });

  $('select[name="edifice"], select[name="dependency"]').on('change', function(){
    updateOfficeOptions($('select[name="edifice"]').val(), $('select[name="dependency"]').val());
  });

  initializeFormSubmission('#myForm', 'edit')
});