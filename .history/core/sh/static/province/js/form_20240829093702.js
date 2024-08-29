function message_error(msg){
  console.error('Errores del formulario recibidos: ', msg);

  if (typeof msg === 'object' && msg.error){
    let errorMessages = "";
    for (let key in msg.error){
      if (msg.error.hasOwnProperty(key) && Array.isArray(msg.error[key])){
        errorMessages += `${key}: ${msg.error[key][0]} \n`;
      }
    }
    alert("Hay errores en el formulario:\n" + errorMessages);
  } else {
    alert(msg);
  }
}