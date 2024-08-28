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

document.addEventListener('DOMContentLoaded', function() {
  let form = document.querySelector('form[data-form-id');
  if (!form) return;

  let hasErrors = form.getAttribute('data-has-errors') === 'true';
  let saved = form.getAttribute('data-saved') ==='true';
  let action = form.getAttribute('data-action');

  if (hasErrors) {
    Swal.fire({
      icon: "error",
      iconColor: "#dc3545",
      title: "Oops...",
      text: "Ha ocurrido un error. Por favor, revise los campos del formulario.",
      confirmButtonColor: "#dc3545",
      background: "#ffffff",
    });

  } else if (saved) {
    let successMessage = action == 'add' ? 'El registro se ha guardado correctamente.' : 'El registro se ha actualizado correctamente';

    Swal.fire({
      icon: "success",
      iconColor: "#28a745",
      title: '¡Perfecto!',
      text: successMessage,
      confirmButtonColor: "#27a745",
      background: "#ffffff",
    });
  }
});

// SUBMITS AJAX

function submit_with_ajax(url, params, callback, actionType = 'add'){

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
      info: {
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
              'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            }
          }).done(function(data){
            if(!data.hasOwnProperty('error')){
              callback();
              $.confirm({
                theme: 'bootstrap',
                title: 'Éxito',
                icon: 'fa fa-check-circle',
                content: 'La operación se realizó con éxito.',
                type: 'green',
                buttons: {
                  ok: {
                    text: "OK",
                    btnClass: 'btn-success',
                    action: function(){
                      window.location.href = $('form[data-list-url]').data('list-url');
                    }
                  }
                }
              });
            } else {
              error_msg(data.error);
            }
          }).fail(function (jqXHR, textStatus, errorThrown) {
            alert(textStatus + ': ' + errorThrown);
          }).always(function(data){
            // código opcional para ejecutar siempre después de la solicitud
          })
        }
      },
      danger: {
        text: "No",
        btnClass: 'btn-danger',
        action: function(){

        }
      },
    }
  })
}

// SELECT2

$(document).ready(function() {
  if ($('.select2').length > 0 && typeof $.fn.select2 !== 'undefined'){
    $('.select2').select2({
      theme:'bootstrap',
    });
  }
});