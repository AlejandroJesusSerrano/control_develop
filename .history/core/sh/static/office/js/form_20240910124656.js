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
    message_error(textStatus + ': ' + errorThrown);
  });
};

// INITALIZE SELECTS

function initializeSelects() {
  const location_id = $('select[name="location"]').val();
  const edifice_id = $('select[name="edifice"]').val();

  if (location_id) {
    updateEdificeOptions(location_id);
    updateDependencyOptions(location_id);
  }

  if (edifice_id) {
    updateOfficeLocationOptions(edifice_id)
  }


}

// UPDATE OPTIONS

function updateDependencyOptions(location_id) {
  if (location_id) {
    updateOptions(window.location.pathname, {
      'action': 'search_dependency',
      'location_id': location_id,
    }, $('select[name="dependency"]'), $('#id_location').data('preselected'));
  } else {
    $('select[name="dependency"]').html('<option value="">----------</option>');
  }
};

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

function updateOfficeLocationOptions(edifice_id) {
  if (edifice_id) {
    updateOptions(window.location.pathname, {
      'action': 'search_loc',
      'edifice_id': edifice_id,
    }, $('select[name="office_loc"]'), $('#id_office_loc').data('preselected'));
  } else {
    $('select[name="office_loc"]').html('<option value="">----------</option>');
  }
};

// START

$(document).ready(function() {
  initializeSelects();

  $('select[name="location"]').on('change', function(){
    updateEdificeOptions($(this).val());
    updateDependencyOptions($(this).val());
  });

  $('select[name="edifice"]').on('change', function(){
    updateOfficeLocationOptions($(this).val());
  });

  initializeFormSubmission('#myForm', 'edit')
});