// SELECT 2

$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  initializeSelects();

  $('select[name="province"]').on('change', function(){
    updateLocationsOptions($(this).val());
  });

  $('select[name="location"]').on('change', function(){
    updateEdificeOptions($(this).val());
  });

  initializeFormSubmission('#myForm', 'edit')
});

// INITIALIZE SELECTS

function initializeSelects() {
  const province_id = $('select[name="province"]').val();
  const location_id = $('select[name="location"]').val();

  if (province_id) {
    updateLocationsOptions(province_id)
  }

  else if (location_id) {
    updateEdificeOptions(location_id)
  }
}

// UPDATE LOCATION & EDIFICE OPTIONS

function updateLocationsOptions(province_id) {
  if (province_id) {
    updateOptions(window.location.pathname, {
      'action': 'search_location',
      'province_Id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
};

function updateEdificeOptions(location_id) {
  if (location_id) {
    updateOptions(window.location.pathname, {
      'action': 'search_edifice',
      'location_id': location_id,
    }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
  }
};

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
          errorHtml += error.message ? error.message + '<br>' : error + '<br>';
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
    dataType: 'json',
    success: function(data) {
      if (data.hasOwnProperty('error')) {
        message_error(data.error)
      } else {
        $.each(data, function(index, value) {
          options += '<option value="' + value.id + '">' + value.name + '</option>';
        });
        selectElement.html(option).trigger('change');

        if (preselectedValue) {
          selectElement.val(preselectedValue).trigger('change');
        }
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      message_error(textStatus + ': ' + errorThrown);
    }
  });
}




