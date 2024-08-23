function message_error(msg){

  console.error('Errores del formulario recibidos: ', msg);

  if (typeof msg === 'object'){
    let errorMessages = "";
    for (let key in msg){
      if (msg.hasOwnProperty(key)){
        errorMessages += `${key}: ${msg[key].join(', ')}\n;`
      }
    }
    alert("Hay errores en el formulario:\n" + errorMessages);
  } else {
    alert(msg);
  }
}

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
      selectElement.html(options);

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
}

$(function(){
  const office_id = $('select[name="office"]').val();
  const brand_id = $('select[name="brand"]').val();
  const dev_type_id = $('select[name="dev_type"]').val();

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
  }

  if (brand_id && dev_type_id) {
    updateOptions(window.location.pathname, {
      'action': 'search_models',
      'dev_type_id': dev_type_id,
      'brand_id': brand_id
    }, $('select[name="dev_model"]'), $('#id_dev_model').data('preselected'));
  }

  $('select[name="office"]').on('change', function(){
    const office_id = $(this).val();

    updateOptions(window.location.pathname, {
      'action': 'search_wall_ports',
      'office_id': office_id
    }, $('select[name="wall_port"]'));

    updateOptions(window.location.pathname, {
      'action': 'search_switch_ports',
      'office_id': office_id
    }, $('select[name="switch_port"]'));

    updateOptions(window.location.pathname, {
      'action': 'search_employees',
      'office_id': office_id
    }, $('select[name="employee"]'));
  });

  $('select[name="dev_type"], select[name="brand"]').on('change', function(){
    const dev_type_id = $('select[name="dev_type"]').val();
    const brand_id = $('select[name="brand"]').val();

    updateOptions(window.location.pathname, {
      'action': 'search_models',
      'dev_type_id': dev_type_id,
      'brand_id': brand_id
    }, $('select[name="dev_model"]'));
  });


  $(document).ready(function() {
    $('.select2').select2({
      theme:'bootstrap4',
    });
  });

});

