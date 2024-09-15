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

  console.log("URL: ", url);
  console.log("Data: ", data);

  $.ajax({
    url: url,
    type: 'POST',
    data: data,
    dataType: 'json'
  }).done(function (data) {

    console.log("Received data: ", data);

    if (typeof data === 'object' && !data.hasOwnProperty('error')) {
      $.each(data, function (key, value) {
        options += '<option value="' + value.id + '">' + value.name + '</option>';
      });
      selectElement.html(options).trigger('change');

      selectElement.trigger('change'); 
      selectElement.select2({
        theme: 'bootstrap'
      });

      if (preselectedValue) {
        selectElement.val(preselectedValue).trigger('change');
      }

      console.log("Updated selectElement: ", selectElement);

    } else if(data.hasOwnProperty('error')) {
      message_error(data.error);

    } else {
      message_error('Ha ocurrido un error inesperado');
    }

  }).fail(function (jqXHR, textStatus, errorThrown) {
    message_error(textStatus + ': ' + errorThrown);
    console.log("Response text: ", jqXHR.responseText);
  });
};

// INITALIZE SELECTS

function initializeSelects() {
  const brand_id = $('select[name="brand"]').val();
  const dev_type_id = $('select[name="dev_type"]').val();
  const dependency_id = $('select[name="dependency"]').val();
  const office_id = $('select[name="office"]').val();

  if (brand_id && dev_type_id) {
    updateModelOptions(brand_id, dev_type_id);
  }

  if (dependency_id) {
    updateOfficeOptions(dependency_id);
  }

  if (office_id) {
    updateOfficeRelatedOptions(office_id);
  }

}

// UPDATE OPTIONS

function updateModelOptions(brand_id, dev_type_id) {
  updateOptions(window.location.pathname, {
    'action': 'search_models',
    'dev_type_id': dev_type_id,
    'brand_id': brand_id
  }, $('select[name="dev_model"]'), $('#id_dev_model').data('preselected'));
};


function updateOfficeOptions(dependency_id) {
  if (dependency_id) {
    updateOptions(window.location.pathname, {
    'action': 'search_office',
    'dependency_id': dependency_id,
    }, $('select[name="office"]'), $('#id_office').data('preselected'));
  } else {
    $('select[name="office"]').html('<option value="">----------</option>');
  }
};

function updateOfficeRelatedOptions(office_id) {
  if (office_id) {
    updateOptions(window.location.pathname, {
    'action': 'search_wall_ports',
    'office_id': office_id,
    }, $('select[name="wall_port"]'), $('#id_wall_port').data('preselected'));

    updateOptions(window.location.pathname, {
    'action': 'search_switch_ports',
    'office_id': office_id
    }, $('select[name="switch_port"]'), $('#id_switch_port').data('preselected'));

    updateOptions(window.location.pathname, {
    'action': 'search_employees',
    'office_id': office_id
    }, $('select[name="employee"]'), $('#id_employee').data('preselected'));
  } else {
    $('select[name="wall_port"], select[name="switch_port"], select[name="employee"]').html('<option value="">----------</option>').trigger('change');
  };
};

// START

$(document).ready(function() {
  initializeSelects();

  $('select[name="dependency"]').on('change', function(){
    updateOfficeOptions($(this).val());
  });

  $('select[name="office"]').on('change', function(){
    updateOfficeRelatedOptions($(this).val());
  });

  $('select[name="dev_type"], select[name="brand"]').on('change', function(){
    updateModelOptions($('select[name="brand"]').val(), $('select[name="dev_type"]').val());
  });

  initializeFormSubmission('#myForm', 'edit')
});