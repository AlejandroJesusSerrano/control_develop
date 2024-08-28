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
  for (let field in errors) {
    if (errors.hasOwnProperty(field)) {
      let fieldElement = document.querySelector(`[name="${field}"]`);
      if (fieldElement) {
        fieldElement.classList.add('is-invalid');
        let errorDiv = document.createElement('div');
        errorDiv.classList.add('invalid-feedback');
        errorDiv.innerHTML = errors[field][0].message;
        fieldElement.parentNode.appendChild(errorDiv);
      }
    }
  }
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
                error_msg(data.error);
                highlight_form_errors(data.error);
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

function highlight_form_errors(errors) {
  for (let field in errors){
    if (errors.hasOwnProperty(field)) {
      let fieldElement = document.querySelector('[name="${field}"]');
      if (fieldElement) {
        fieldElement.classList.add('is-invalid');
      }
    }
  }
}

// SELECT2

$(document).ready(function() {
    $('.select2').select2({
      theme:'bootstrap',
    });
});