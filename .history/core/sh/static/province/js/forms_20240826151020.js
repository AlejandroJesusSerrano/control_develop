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