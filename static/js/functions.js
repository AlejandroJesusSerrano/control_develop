function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let c = 0; c < cookies.length; c++) {
      const cookie = cookies[c].trim();

      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

window.csrftoken = window.csrftoken || getCookie('csrftoken');



$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!this.crossDomain && !/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$(document).ready(function () {
  const body = $('body');
  const sidebar = $('.main-sidebar');

  // Detectar cuando el mouse entra en el sidebar
  sidebar.hover(
    function () {
        if (body.hasClass('sidebar-mini')) {
            body.removeClass('sidebar-collapse').addClass('sidebar-open');
        }
    },
  );
});


function show_errors_in_form(errors) {

  $('.is-invalid').removeClass('is-invalid');
  $('.invalid-feedback').remove();

  $.each(errors, function (field, messages) {
    let fieldElement = $('[name="' + field + '"]');

    if (fieldElement.length > 0) {
      fieldElement.addClass('is-invalid');
      let errorHtml = '<div class="invalid-feedback d-block">';

      $.each(messages, function (index, errorObj) {
        errorHtml += errorObj.message + '<br>';
      });

      errorHtml += '</div>';
      fieldElement.after(errorHtml)
    }
  });
}


function message_error(msg) {
  console.error('Errores recibidos: ', msg)

  if (typeof msg === 'object' && msg.hasOwnProperty('error')) {
    show_errors_in_form(msg.error);
  } else if (typeof msg === 'object') {
    show_errors_in_form(msg)
  } else if (typeof msg === 'string') {
    alert(msg);
  } else {
    alert('Ha ocurrido un error inesperado en el servidor.');
  }

}

window.activeRequests = window.activeRequests || {};

function updateOptions(url, data, selectElement, preselectedVal = null) {
  const selectId = selectElement.attr('id');

  // Chequeo de activeRequests, etc. (igual que tu código)
  if (activeRequests[selectId]) {
    console.log(`Solicitud activa ya existente para ${selectId}, abortando.`);
    return;
  }
  activeRequests[selectId] = true;

  let options = '<option value="">----------</option>';
  // Si no me pasan preselectedVal, uso .val() del select
  if (preselectedVal === null) {
    preselectedVal = selectElement.val() || '';
  }

  $.ajax({
    url: url,
    type: 'POST',
    data: data,
    dataType: 'json',
  })
  .done(function (response) {
    if (Array.isArray(response)) {
      response.forEach(item => {
        // Compara ID de la BD con preselectedVal
        const selected = (String(item.id) === String(preselectedVal)) ? 'selected' : '';

        // dev_str extra, si usas data-devtype
        let devStrAttr = '';
        if (item.dev_str) {
          devStrAttr = ` data-devtype="${item.dev_str}"`;
        }

        options += `<option value="${item.id}" ${selected}${devStrAttr}>${item.name}</option>`;
      });
      selectElement.html(options).trigger('change.select2');
    } else {
      console.error('Error en respuesta:', response);
    }
  })
  .fail(function (jqXHR, textStatus) {
    console.error(`Error en solicitud AJAX para ${selectId}:`, textStatus);
  })
  .always(function () {
    activeRequests[selectId] = false;
  });
}




function confirmAndSend(url, title, icon, content, type, formData, callback) {
  $.confirm({
    theme: 'supervan',
    title: title,
    icon: icon,
    content: content,
    type: type,
    columnClass: 'medium',
    typeAnimated: true,
    dragWindowBorder: false,
    buttons: {
      info: {
        text: "Sí",
        btnClass: 'btn-primary',
        action: function () {

          $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            dataType: 'json',
            processData: false,
            contentType: false,
          }).done(function (data) {
            console.log('confirmAndSend → .done(...) data = ', data);
            if (!data.hasOwnProperty('error')) {
              callback(data);
            } else {
              message_error(data.error);
            }
          }).fail(function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 403) {
              message_error("Error de seguridad: token CSRF inválido no proporcionado.");
            } else if (jqXHR.status === 400) {
              let response = jqXHR.responseJSON;
              if (response && response.error) {
                message_error(response.error);
              } else {
                message_error('Ha ocurrido un error en la validación del formulario.');
              }
            } else {
              message_error(textStatus + ': ' + errorThrown);
            }
          });
        }
      },
      danger: {
        text: "No",
        btnClass: 'bg-custom-danger',
        action: function () {

        }
      },
    }
  });
}

function submit_with_ajax(url, formData, callback, actionType = 'add') {
  let title, icon, content, type;

  switch (actionType) {
    case 'edit':
      title = 'Confirmación de actualización';
      icon = 'fa fa-edit';
      content = 'Ud va a modificar un registro en la base de datos. ¿Desea continuar?';
      type = 'orange';
      break;
    case 'delete':
      title = 'Confirmación de eliminación';
      icon = 'fa fa-trash';
      content = 'El registro que está por borrar no podrá ser recuperado. ¿Está seguro de continuar?';
      type = 'red';
      break;
    case 'add':
    default:
      title = 'Confirmación de creación';
      icon = 'fa fa-info';
      content = 'Ud va a generar un nuevo registro en la base de datos. ¿Desea continuar?';
      type = 'blue';
      break;
  }

  confirmAndSend(url, title, icon, content, type, formData, callback);
}

function clearDependentFields(fields){
  fields.forEach(field => {
    if(!['#if_office', '#id_rack'].includes(field)) {
      $(field).val(null).trigger('change.select2');
    }
  });
}

$('#submitButton').on('click', function (e) {
  e.preventDefault();

  var form = $('#form');
  var formData = new FormData(form[0]);
  var url = form.attr('action');

  var callback = function () {
    alert('Operación realizada exitosamente.');
    window.location.reload();
  };

  submit_with_ajax(url, formData, callback, 'add');
});

$('.select2').each(function () {
  const preselectedValue = $(this).data('preselected');
  if (preselectedValue) {
    $(this).val(preselectedValue).trigger('change.select2');
  }
});


