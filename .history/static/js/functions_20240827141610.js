// GET CSRF TOKEN

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
const csrftoken = getCookie('csrftoken')

$.ajaxSetup({
  headers: {
    "X-CSRFToken": csrftoken
  }
});

// ERROR MSG

function error_msg(obj) {
  let html = '<ul class="text-center">';

  $.each(obj, function (key, value) {

    if (Array.isArray(value) && value.length > 0) {
      let message = value[0].message ? value[0].message : value[0];
      html += `<li>${key}: ${message}</li>`;
    } else {
      html += `<li>${key}: Error desconocido</li>`;
    }
  });

  html += '</ul>';

  Swal.fire({
    icon: "error",
    iconColor: "#dc3545",
    title: "Oops...",
    html: html,
    confirmButtonColor: "#dc3545",
    background: "#ffffff",
  });
}
// SUBMITS AJAX

function submit_with_ajax(url, params, callback, actionType = 'add') {

  let title, icon, content, type;

  switch(actionType) {
    case 'edit':
      title = 'Confirmación de actualización';
      icon = 'fa fa-edit';
      content = 'Ud va a modificar un registro en la base de datos. ¿Desea continuar?';
      type = 'orange'
      break;
    case 'delete':
      title = 'Confirmación de eliminación';
      icon = 'fa fa-trash';
      content = 'El registro que esta por borrar no podra ser recuperado. ¿Esta seguro de continuar?';
      type = 'red'
      break;
    case 'add':
    default:
      title = 'Confirmación de creación';
      icon = 'fa fa-info';
      content = 'Ud va a generar un nuevo registro en la base de datos. ¿Desea continuar?';
      type = 'blue'
      break;
  }

  $.confirm({
    theme: 'bootstrap',
    title: title,
    icon: icon,
    content: content,
    type: type,
    columnClass: 'medium',
    typeAnimated: true,
    dragWindowsBorder: false,
    buttons: {
      confirm: {
        text: "Si",
        btnClass: 'btn-primary',
        action: function(){
          $.ajax({
            url: url,
            type: 'POST',
            data: params,
            processData: false,
            contentType: false,
            dataType: 'json',
            headers: {
              'X-CSRFToken': csrftoken
            }
          }).done(function(data){
            if(!data.hasOwnProperty('error')){
              callback();
              } else {
                show_errors_in_form(data.error);
              }
            }).fail(function (jqXHR, textStatus, errorThrown) {

            alert(textStatus+': ' +errorThrown);

          });

        }

      },
      cancel: {
        text: "No",
        btnClass: 'btn-danger',
        action: function(){

        }
      },
    }
  })
}

function show_errors_in_form(errors){
  $('.is-invalid').removeClass('is-invalid');
  $('.invalid-feedback').remove()

$.each(errors, function(field, messages) {
  let fieldElement = $(`[name="${field}"]`);
  if (fieldElement.length > 0) {
    fieldElement.addClass('is-invalid');
    fieldElement.after(`<div class="invalid-feedback">${messages.join('<br>')}</div>`);
  }
})
}




// SELECT2

$(document).ready(function() {
    $('.select2').select2({
      theme:'bootstrap',
    });
});