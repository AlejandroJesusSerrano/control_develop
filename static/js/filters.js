$(document).ready(function() {
    // Inicializar Select2
    $('.select2').select2({
        theme: 'bootstrap',
    });

    // Evento para province
    if ($('#id_province').length > 0) {
        $('select[name="province"]').on('change', function() {
            const province_id = $(this).val();
            console.log('Provincia seleccionada con ID:', province_id);
            updateLocationOptions(province_id);
        });
    }

    // Evento para location
    if ($('#id_location').length > 0) {
        $('select[name="location"]').on('change', function() {
            const location_id = $(this).val();
            console.log('Localidad seleccionada con ID:', location_id);
            updateLocationReferedOptions(location_id);
        });
    }

    // Evento para edifice
    if ($('#id_edifice').length > 0) {
        $('select[name="edifice"]').on('change', function() {
            const edifice_id = $(this).val();
            console.log('Edificio seleccionado con ID:', edifice_id);
            updateEdificeOptions(edifice_id);
        });
    }

    // Evento para dependency
    if ($('#id_dependency').length > 0) {
        $('select[name="dependency"]').on('change', function() {
            const dependency_id = $(this).val();
            console.log('Dependencia seleccionada con ID:', dependency_id);
            updateDependencyOptions(dependency_id);
        });
    }

    // Evento para loc
    if ($('#id_loc').length > 0) {
        $('select[name="loc"]').on('change', function() {
            const loc_id = $(this).val();
            console.log('Ubicación de oficina seleccionada con ID:', loc_id);
            updateLocOptions(loc_id);
        });
    }

    // Funciones de actualización
    function updateLocationOptions(province_id) {
        if (province_id) {
            updateOptions('/sh/ajax/load_location/', {
                'province_id': province_id,
            }, $('select[name="location"]'), $('#id_location').data('preselected'));
            // Disparar cambio en location para propagar la actualización
            $('select[name="location"]').trigger('change');
        } else {
            clearDependentFields(['#id_location', '#id_edifice', '#id_dependency', '#id_loc', '#id_office']);
        }
    }

    function updateLocationReferedOptions(location_id) {
        if (location_id) {
            updateOptions('/sh/ajax/load_edifices/', {
                'location_id': location_id,
            }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
            updateOptions('/sh/ajax/load_edifices/', {
                'location_id': location_id,
            }, $('select[name="edifice_port"]'), $('#id_edifice_port').data('preselected'));
            updateOptions('/sh/ajax/load_dependency/', {
                'location_id': location_id,
            }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
            // Disparar cambios en edifice y dependency
            $('select[name="edifice"]').trigger('change');
            $('select[name="edifice_port"]').trigger('change');
            $('select[name="dependency"]').trigger('change');
        } else {
            clearDependentFields(['#id_edifice', '#id_edifice_port', '#id_dependency', '#id_loc', '#id_office']);
        }
    }

    function updateEdificeOptions(edifice_id) {
        if (edifice_id) {
            updateOptions('/sh/ajax/load_loc/', {
                'edifice_id': edifice_id,
            }, $('select[name="loc"]'), $('#id_loc').data('preselected'));
            // Disparar cambio en loc
            $('select[name="loc"]').trigger('change');
        } else {
            clearDependentFields(['#id_loc', '#id_office']);
        }
    }

    function updateDependencyOptions(dependency_id) {
        if (dependency_id) {
            updateOptions('/sh/ajax/load_office/', {
                'dependency_id': dependency_id,
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        } else {
            clearDependentFields(['#id_office']);
        }
    }

    function updateLocOptions(loc_id) {
        if (loc_id) {
            updateOptions('/sh/ajax/load_office/', {
                'loc_id': loc_id,
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        } else {
            clearDependentFields(['#id_office']);
        }
    }

    // Función para limpiar campos dependientes
    function clearDependentFields(fieldIds) {
        fieldIds.forEach(function(fieldId) {
            $(fieldId).val(null).trigger('change');
        });
    }
});
