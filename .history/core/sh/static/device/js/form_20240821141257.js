//  static/device/form.js

// csfr

function getCookie(name){
  let cookieValue = null;
  if (document.cookie && document.cookie !== ''){
    const cookies = document.cookie.split(';');
    for (let c = 0; c < cookies.length; c++){
      const cookie = cookies[c].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  headers: {
    "X-CSRFToken": csrftoken
  }
});

function message_error(msg){
  console.error(msg);
  alert(JSON.stringify(msg, null, 2))
  alert(msg);
}

function updateOptions(url, data, selectElement) {
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
    } else {
      message_error(data.error || 'Ha ocurrido un error inesperado');
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
    }), $('select[name="dev_model"]')
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
});