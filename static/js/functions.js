function error_msg(obj) {
  let html = '<ul class="text-center">';
  $.each(obj, function (key, value) {
    if (typeof (obj) === 'object' && value !== null) {
      value = value[0].message;
    }
    html+='<li>' +key+': '+value+'</li>';
  });
  html+='</ul>';
  Swal.fire({
    icon: "error",
    iconColor: "#dc3545",
    title: "Oops...",
    html: html,
    confirmButtonColor: "#dc3545",
    background: "#ffffff",
  })
}

function submit_whit_ajax(url, params, callback, actionType = 'add'){

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
              } else {
                error_msg(data.error);
              }
            }).fail(function (jqXHR, textStatus, errorThrown) {a

            alert(textStatus+': ' +errorThrown);

          }).always(function(data){

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
