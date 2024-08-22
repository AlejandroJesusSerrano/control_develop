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

function updateOptions(url, data, selectElement) {
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

    } else if(data.hasOwnProperty('error')) {
      message_error(data.error);

    } else {
      message_error('Ha ocurrido un error inesperado');
    }

  }).fail(function (jqXHR, textStatus, errorThrown) {
    message_error(textStatus + ': ' + errorThrown);
  });
}

$(function(){
  const office_id = $('select[name="office"]').val();
  const brand_id = $('select[name="brand"]').val();
  const dev_type_id = $('select[name="dev_type"]').val();

  if (office_id) {
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
  }

  if (brand_id && dev_type_id) {
    updateOptions(window.location.pathname, {
      'action': 'search_models',
      'dev_type_id': dev_type_id,
      'brand_id': brand_id
    }, $('select[name="dev_model"]'));
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

  const formElement = $('form[data-form-id]');
  const formId = formElement.data('form-id');
  const listUrl = formElement.data('list-url');

  console.log("Form ID: ", formId)
  console.log("List URL: ", listUrl)

  console.log("Form elements: ", formElement.serializeArray());

  formElement.on('submit', function(e) {
    e.preventDefault();

    let params = new FormData(this);

    params.forEach(function(value, key){
      console.log(key + ': ' + value);
    })

    let actionType = formId;

    console.log("Submitting with the following data: ");
    params.forEach((value, key) => {
      console.log(key, ":", value);
    });

    submit_with_ajax(window.location.pathname, params, function(data){
      window.location.href = formElement.data('list_url');
    }, actionType);
  });
});

