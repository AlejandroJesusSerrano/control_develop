function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let c = 0; c < cookies.length; c++) {
      const cookie = cookies[c].trim();
      // ¿Comienza esta cookie con el nombre que queremos?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!this.crossDomain && !/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
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

function updateOptions(url, data, selectElement, preselectedValue) {
  let options = '<option value="">----------</option>';

  $.ajax({
    url: url,
    type: 'POST',
    data: data,
    dataType: 'json',
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

    } else if (data.hasOwnProperty('error')) {
      message_error(data.error);
    } else {
      message_error('Ha ocurrido un error inesperado');
    }
  }).fail(function (jqXHR, textStatus, errorThrown) {
    if (jqXHR.status == 403) {
      message_error('Error de seguridad: token CSRF inválido o no proporcionado.');
    } else if (jqXHR.status === 400) {
      let response = jqXHR.responseJSON;
      if (response && response.errors) {
        message_error(response);
      } else {
        message_error('Ha ocurrido un error en la validación del formulario.');
      }
    } else {
      message_error(textStatus + ': ' + errorThrown);
    }
  });
}


function confirmAndSend(url, title, icon, content, type, formData, callback) {
  $.confirm({
    theme: 'bootstrap',
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
            if (!data.hasOwnProperty('error')) {
              callback();
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
        btnClass: 'btn-danger',
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
    $(field).val(null).trigger('change');
  });
}


$(document).ready(function () {
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
});