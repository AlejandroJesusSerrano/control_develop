$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#custom_file_button').click(function() {
    $('#id_image_selector').click();
  });

  $('#id_image_selector').change(function() {
    const fileName = $(this).val().split('\\').pop();
    $('#file_name').text(fileName || 'Ningún archivo seleccionado');
  });

  $('#brand_popup_add').on('click', function() {
    let url = brandAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Marca', 'width=800,height=250');
    popup.focus();
  });

  $('#dev_type_popup_add').on('click', function() {
    let url = dev_typeAddUrl + "?popup=1";
    let popup = window.open(url, 'Agregar Tipo de Dispositivo', 'width=800,height=250');
    popup.focus();
  });

  window.addEventListener('message', function(event) {
    if (event.data.type === 'brandAdded') {
        let brandId = event.data.id;
        let brandName = event.data.name;
        let select = $('#id_brand');
        let option = new Option(brandName, brandId, true, true);
        select.append(option).val(brandId).trigger('change');
    }

    if (event.data.type === 'dev_typeAdded') {
      let dev_typeId = event.data.id;
      let dev_typeName = event.data.name;
      let select = $('#id_dev_type');
      let option = new Option(dev_typeName, dev_typeId, true, true);
      select.append(option).val(dev_typeId).trigger('change');
    }

  });

  initializeFormSubmission('#myform', 'edit');

});

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
      e.preventDefault();

      let formData = new FormData(this);

      submit_with_ajax($(this).attr('action'), formData, function() {
          console.log('Formulario enviado y procesado con éxito');
          window.location.href = '/sh/wall_port/list/';
      }, actionType);
  });
}
