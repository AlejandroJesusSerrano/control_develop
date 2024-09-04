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
    updateOptions(window.location.pathname, {
    'action': 'search_location',
    'province_id': province_id,
    }, $('select[name="location"]'), $('#id_location').data('preselected'));
  } else {
    $('select[name="location"]').html('<option value="">----------</option>');
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
