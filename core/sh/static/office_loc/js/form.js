$(document).ready(function() {
  $('.select2').select2({
    theme:'bootstrap',
  });

  $('#toggle-edifice-filters').on('click', function (e) {
    e.preventDefault();
    const filterEdifCards = $('#filter-edifice-cards')
    filterEdifCards.toggleClass('d-none')

    $(this).toggleClass('active btn-primary btn-secondary')

    if (filterEdifCards.hasClass('d-none')) {
      $(this).html('Filtros de Edificios <i class="fas fa-search"></i>');
    } else {
      $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
    }
  });

  const selectMapping = {
    province: ['location', 'edifice'],
    location: ['edifice']
  };

  $('select[name="province"], select[name="location"]').on('change', function(){
    const fieldName = $(this).attr('name');
    const fieldsToClear = selectMapping[fieldName] || [];
    clearDependentFields(fieldsToClear.map(field => `select[name="${field}"]`));

    switch (fieldName) {
      case 'province':
        updateLocationOptions();
        updateEdificeOptions();
        break;

      case 'location':
        updateEdificeOptions();
        break;
    }

  });

  initializeFormSubmission('#myform', 'edit');

});

function updateLocationOptions() {
  const { province_id } = getSelectedFilters();
  if (province_id) {
    updateOptions('/sh/ajax/load_location/', { province_id }, $('select[name="location"]'), $('#id_location').data('preselected'));
  }
};

function updateEdificeOptions() {
  const { province_id, location_id } = getSelectedFilters();
  const data = location_id ? { location_id } : province_id ? { province_id }: {};
  if (Object.keys(data).length > 0) {
    updateOptions('/sh/ajax/load_edifices/', data, $('select[name="edifice"]'), $('#id_edifice').data ('preselected'));
  }
};

function filterNonEmpty(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([_, value]) => value));
}

function getSelectedFilters() {
  return {
    province_id: $('select[name="province"]').val(),
    location_id: $('select[name="location"]').val(),
    edifice_id: $('select[name="edifice"]').val()
  };
}

function initializeFormSubmission(formSelector, actionType) {
  $(formSelector).on('submit', function(e) {
    e.preventDefautlt();

    let formData = new FormData(this);

    submit_with_ajax($(this).attr('action'), formData, function() {
      console.log('Formulario enviado y procesado con éxito');
      window.location.href = '/sh/office_loc/list';
    }, actionType)
  });
}