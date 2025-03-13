$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('select[name="rack"]').on('change', function(){
    const rack_id = $(this).val();
    updateRackOptions(rack_id);
  });

  $('#rack_popup_add').on('click', function (){
    let url = rackAddUrl + "?popup=1";
    let popup = window.open(url, 'rack_add_popup', 'width=800,height=600');
    popup.focus();
  });

  $('#patchera_popup_add').on('click', function (){
    let url = patcheraAddUrl + "?popup=1";
    let popup = window.open(url, 'patchera_add_popup', 'width=800,height=300');
    popup.focus();
  });

  window.addEventListener('message', function(event) {
    if (event.data.type === 'rackAdded') {
        let rackId = event.data.id;
        let rackName = event.data.name;
        let select = $('#id_rack');
        let option = new Option(rackName, rackId, true, true);
        select.append(option).trigger('change');
        select.select2({theme: 'bootstrap'});
    }

    if (event.data.type === 'patcheraAdded') {
        let patcheraId = event.data.id;
        let patcheraName = event.data.name;
        let select = $('#id_patchera');
        let option = new Option(patcheraName, patcheraId, true, true);
        select.append(option).trigger('change');
        select.select2({theme: 'bootstrap'});
    }
});


  initializeFormSubmission('#myform', 'edit');
});

function updateRackOptions(rack_id){
  if (rack_id) {
    updateOptions('/sh/ajax/load_patchera/', {
      'rack_id': rack_id,
    }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
  }
};

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/patch_port/list';
    }, actionType)
  });
}