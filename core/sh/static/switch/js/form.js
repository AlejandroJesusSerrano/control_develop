$(document).ready(function() {
    $('.select2').select2({
        theme: 'bootstrap',
    });

    updateSwitchBrandOptions();

    updateSwitchPortsOptions(null);
    updatePatcheraPortsOptions(null);

    if ($('#id_edifice_ports').length > 0) {
            $('select[name="edifice_ports"]').on('change', function() {
            const edifice_ports_id = $(this).val();
            updateEdificePortsOptions(edifice_ports_id);
        });
    }

    if ($('#id_loc_ports').length > 0) {
        $('select[name="loc_ports"]').on('change', function() {
            const loc_ports_id = $(this).val();
            updateLocPortsOptions(loc_ports_id);
        });
    }

    if ($('#id_office_ports').length > 0) {
        $('select[name="office_ports"]').on('change', function() {
            const office_ports_id = $(this).val();
            updateOfficePortsOptions(office_ports_id);
        });
    }

    if ($('#id_rack_ports').length > 0) {
        $('select[name="rack_ports"]').on('change', function() {
            const rack_ports_id = $(this).val();
            updateRackPortsOptions(rack_ports_id);
        });
    }

    if ($('#id_brand').length > 0) {
        $('select[name="brand"]').on('change', function() {
            const brand_id = $(this).val();
            updateSwitchModelOptions(brand_id);
        });
    }

    $('select[name="switch_ports"]').on('change', function() {
        const switch_id = $(this).val();
        updateSwitchPortsOptions(switch_id);
    });


    $('select[name="patchera_ports"]').on('change', function() {
        const patchera_id = $(this).val();
        updatePatcheraPortsOptions(patchera_id);
    });

    togglePosFields()

    togglePortFields();

    $('select[name="wall_port_in"], select[name="switch_ports"], select[name="switch_port_in"], select[name="patchera_ports"], select[name="patch_port_in"], select[name="rack_ports"]').on('change', function() {
        if (!isToggling) {
            togglePortFields()
        }
    });

    $('select[name="office"], select[name="rack"]').on('change', function() {
        if (!posIsToggling) {
            togglePosFields();
        }
    });

    $('input[name="switch_rack_pos"]').on('input', function() {
        if (!posIsToggling) {
            togglePosFields();
        }
    });

    $('#toggle-office-filters').on('click', function (e) {
        e.preventDefault();
        const filterLocCards = $('#filter-office-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros de oficinas <i class="fas fa-search"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });

    $('#toggle-ports-filters').on('click', function (e) {
        e.preventDefault();
        const filterPortCards = $('#filter-port-cards')
        filterPortCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterPortCards.hasClass('d-none')) {
            $(this).html('Filtros para puertos <i class="fas fa-search"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });


    $('#brand_popup_add').on('click', function() {
        let url = brandAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Marca', 'width=800,height=250');
        popup.focus();
    });

    $('#dev_model_popup_add').on('click', function() {
        let url = modelAddUrl + "?popup=1&context=switch";
        let popup = window.open(url, 'Agregar Modelo', 'width=800,height=500');
        popup.focus();
    });

    $('#office_popup_add').on('click', function() {
        let url = officeAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Oficina', 'width=800,height=800');
        popup.focus();
    });

    $('#rack_popup_add').on('click', function() {
        let url = rackAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Rack', 'width=800,height=600');
        popup.focus();
    });

    $('#wall_port_popup_add').on('click', function() {
        let url = wallPortAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Boca de Pared', 'width=800,height=900');
        popup.focus();
    });

    $('#switch_port_popup_add').on('click', function() {
        let url = switchPortAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Puerto de Switch', 'width=800,height=700');
        popup.focus();
    });

    $('#patch_port_popup_add').on('click', function() {
        let url = patchPortAddUrl + "?popup=1";
        let popup = window.open(url, 'Agregar Puerto de Patchera', 'width=800,height=400');
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

        if (event.data.type === 'dev_modelAdded') {
            let dev_modelId = event.data.id;
            let dev_modelName = event.data.name;
            let select = $('#id_dev_model');
            let option = new Option(dev_modelName, dev_modelId, true, true);
            select.append(option).val(dev_modelId).trigger('change');
            select.value = dev_modelId;
        }

        if (event.data.type === 'officeAdded') {
            let officeId = event.data.id;
            let officeName = event.data.name;
            let select = $('#id_office');
            let option = new Option(officeName, officeId, true, true);
            select.append(option).val(officeId).trigger('change');
        };

        if (event.data.type === 'rackAdded') {
            let rackId = event.data.id;
            let rackName = event.data.name;
            let select = $('#id_rack');
            let option = new Option(rackName, rackId, true, true);
            select.append(option).val(rackId).trigger('change');
        };

        if (event.data.type === 'wall_portAdded') {
            let wall_portId = event.data.id;
            let wall_portName = event.data.name;
            let select = $('#id_wall_port_in');
            let option = new Option(wall_portName, wall_portId, true, true);
            select.append(option).val(wall_portId).trigger('change');
        };

        if (event.data.type === 'switch_portAdded') {
            let switch_portId = event.data.id;
            let switch_portName = event.data.name;
            let select = $('#id_switch_port_in');
            let option = new Option(switch_portName, switch_portId, true, true);
            select.append(option).val(switch_portId).trigger('change');
        };

        if (event.data.type === 'patch_portAdded') {
            let patch_portId = event.data.id;
            let patch_portName = event.data.name;
            let select = $('#id_patch_port_in');
            let option = new Option(patch_portName, patch_portId, true, true);
            select.append(option).val(patch_portId).trigger('change');
        };
    });

    $('select[name="dev_type"]').on('change', function() {
        const dev_type_val = $(this).val();
        updateOptions('/sh/ajax/load_brand/', {
            usage: 'switch',
            dev_type_name: dev_type_val
        }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
    });

    initializeFormSubmission('#myform', 'edit');

});

let posIsToggling = false;

function togglePosFields() {
    if (posIsToggling) return;
    posIsToggling = true;

    const officeValue = $('select[name="office"]').val();
    const rackValue = $('select[name="rack"]').val();
    const rackPosValue = $('input[name="switch_rack_pos"]').val();

    $('input[name="switch_rack_pos"]').prop('disabled', false);
    $('select[name="rack"]').prop('disabled', false);
    $('select[name="office"]').prop('disabled', false);


    if (officeValue) {
        $('select[name="rack"]').prop('disabled', true).val('').trigger('change.select2');
        $('input[name="switch_rack_pos"]').prop('disabled', true).val('');
    }

    else if (rackValue || rackPosValue) {
        $('select[name="office"]').prop('disabled', true).val('').trigger('change.select2');
        console.log("Office disabled:", $('select[name="office"]').prop('disabled'));

    } else {
        $('input[name="switch_rack_pos"]').prop('disabled', false);
        $('select[name="rack"]').prop('disabled', false);
        $('select[name="office"]').prop('disabled', false);
    }

    $('select[name="office"], select[name="rack"]').trigger('change.select2');

    posIsToggling = false;
}

let isToggling = false;

function togglePortFields() {
    if (isToggling) return;
    isToggling = true;

    const rackPortValue = $('select[name="rack_ports"]').val();
    const wallPortValue = $('select[name="wall_port_in"]').val();
    const switchPortValue = $('select[name="switch_ports"]').val();
    const switchPortInValue = $('select[name="switch_port_in"]').val();
    const patcheraPortValue = $('select[name="patchera_ports"]').val();
    const patchPortInValue = $('select[name="patch_port_in"]').val();

    $('select[name="wall_port_in"]').prop('disabled', false);
    $('select[name="switch_ports"]').prop('disabled', false);
    $('select[name="switch_port_in"]').prop('disabled', false);
    $('select[name="patchera_ports"]').prop('disabled', false);
    $('select[name="patch_port_in"]').prop('disabled', false);


    if (rackPortValue) {
        $('select[name="wall_port_in"]').prop('disabled', true).val(null);
    }


    if (wallPortValue) {
        $('select[name="switch_ports"]').prop('disabled', true).val(null);
        $('select[name="switch_port_in"]').prop('disabled', true).val(null);
        $('select[name="patchera_ports"]').prop('disabled', true).val(null);
        $('select[name="patch_port_in"]').prop('disabled', true).val(null);
    }

    if (switchPortValue) {
        $('select[name="wall_port_in"]').prop('disabled', true).val(null);
        $('select[name="patchera_ports"]').prop('disabled', true).val(null);
        $('select[name="patch_port_in"]').prop('disabled', true).val(null);
        $('select[name="switch_port_in"]').prop('disabled', false);
    }

    if (switchPortInValue) {
        $('select[name="wall_port_in"]').prop('disabled', true).val(null);
        $('select[name="patchera_ports"]').prop('disabled', true).val(null);
        $('select[name="patch_port_in"]').prop('disabled', true).val(null);
        $('select[name="switch_ports"]').prop('disabled', false);
    }

    if (patcheraPortValue) {
        $('select[name="wall_port_in"]').prop('disabled', true).val(null);
        $('select[name="switch_ports"]').prop('disabled', true).val(null);
        $('select[name="switch_port_in"]').prop('disabled', true).val(null);
        $('select[name="patch_port_in"]').prop('disabled', false);
    }

    if (patchPortInValue) {
        $('select[name="wall_port_in"]').prop('disabled', true).val(null);
        $('select[name="switch_ports"]').prop('disabled', true).val(null);
        $('select[name="switch_port_in"]').prop('disabled', true).val(null);
        $('select[name="patchera_ports"]').prop('disabled', false);
    }

    $('select[name="wall_port_in"], select[name="switch_ports"], select[name="switch_port_in"], select[name="patchera_ports"], select[name="patch_port_in"]').trigger('change.select2');

    isToggling = false;
}


function updateEdificePortsFromLocation(location_id) {
    if (location_id) {

        if ($('#id_edifice_ports').length > 0) {
            updateOptions('/sh/ajax/load_edifices/', {
                'location_id': location_id
            }, $('select[name="edifice_ports"]'), $('#id_edifice_ports').data('preselected'));
        }

    } else {
        clearDependentFields(['#id_edifice_ports', '#id_loc_ports', '#id_office_ports', '#id_rack_ports']);
    }
}

function updateEdificePortsOptions(edifice_ports_id) {
    if (edifice_ports_id) {
        if ($('#id_loc_ports').length > 0) {
            updateOptions('/sh/ajax/load_loc/', {
                'edifice_id': edifice_ports_id
            }, $('select[name="loc_ports"]'), $('#id_loc_ports').data('preselected'));
        }
    } else {
        clearDependentFields(['#id_loc_ports', '#id_office_ports', '#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
    }
}

function updateLocPortsOptions(loc_ports_id) {
    if (loc_ports_id) {
        if ($('#id_office_ports').length > 0) {
            updateOptions('/sh/ajax/load_office/', {
                'loc_id': loc_ports_id
            }, $('select[name="office_ports"]'), $('#id_office_ports').data('preselected'));
        }
    } else {
        clearDependentFields(['#id_office_ports', '#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
    }
}

function updateOfficePortsOptions(office_ports_id) {

    const rackPortSelect = $('select[name="rack_ports"]');
    const exclude_switch_id = $('#switch-form').data('switch-id') || null;


    if (office_ports_id) {

        updateOptions('/sh/ajax/load_rack/', {
            'office_id': office_ports_id
        }, rackPortSelect, rackPortSelect.data('preselected'));

        updateOptions('/sh/ajax/load_wall_port/', {
            'office_id': office_ports_id
        }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));

        updateOptions('/sh/ajax/load_switch/', {
            'office_id': office_ports_id,
            'exclude_switch_id': exclude_switch_id
        }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));

        updateOptions('/sh/ajax/load_patchera/', {
            'office_id': office_ports_id
        }, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));


    } else {
        updateOptions('/sh/ajax/load_rack/', {}, rackPortSelect, rackPortSelect.data('preselected'));
        clearDependentFields(['#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
    }
}

function updateRackPortsOptions(rack_ports_id) {

    const switchPortsSelect = $('select[name="switch_ports"]');
    const patcheraPortsSelect = $('select[name="patchera_ports"]');
    const exclude_switch_id = $('#switch-form').data('switch-id') || null;

    if (rack_ports_id) {
        updateOptions('/sh/ajax/load_switch/', {
            'rack_id': rack_ports_id,
            'exclude_switch_id': exclude_switch_id,
        },
            switchPortsSelect,
            switchPortsSelect.data('preselected')
        );
        updateOptions('/sh/ajax/load_patchera/',
            {'rack_id': rack_ports_id},
            patcheraPortsSelect,
            patcheraPortsSelect.data('preselected')
        );
    } else {
        updateOptions('/sh/ajax/load_switch/', {
            'exclude_switch_id': exclude_switch_id
        },
            switchPortsSelect,
            switchPortsSelect.data('preselected')
        ).done(function(response) {

        });
        updateOptions('/sh/ajax/load_patchera/',
            {},
            patcheraPortsSelect,
            patcheraPortsSelect.data('preselected')
        ).done(function(response) {

        });
    }

    $('select[name="switch_port_in"]').val(null).trigger('change.select2');
    $('select[name="patch_port_in"]').val(null).trigger('change.select2');

    togglePortFields();
}

function updateSwitchPortsOptions(switch_id) {
    const exclude_switch_id = $('#switch-form').data('switch-id') || null;
    let params = {
        'exclude_switch_id': exclude_switch_id
    };
    if (switch_id !== undefined && switch_id !== null) {
        params['switch_id'] = switch_id;
    }

    updateOptions('/sh/ajax/load_switch_port/', params, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
    togglePortFields();
}

function updatePatcheraPortsOptions(patchera_id) {
    let office_id = $('select[name="office_ports"]').val();
    let rack_id = $('select[name="rack_ports"]').val();
    let location_id = $('select[name="location"]').val();
    let params = {
        'patchera_id': patchera_id,
        'office_id': office_id,
        'rack_id': rack_id,
        'location_id': location_id
    };
    if (patchera_id !== undefined && patchera_id !== null) {
        params['patchera_id'] = patchera_id;
    }
    updateOptions('/sh/ajax/load_patch_ports/', params, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
    togglePortFields();
}

function updateSwitchBrandOptions() {
    const dev_type_name = 'SWITCH';
    updateOptions('/sh/ajax/load_brand/', {
        'dev_type_name': dev_type_name
    }, $('select[name="brand"]'), $('#id_brand').data('preselected'));
}

function updateSwitchModelOptions(brand_id) {
    const dev_type_name = 'SWITCH';
    updateOptions('/sh/ajax/load_model/', {
        'brand_id': brand_id,
        'dev_type_name': dev_type_name
    }, $('select[name="model"]'), $('#id_model').data('preselected'));
}

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        submit_with_ajax($(this).attr('action'), formData, function() {
        window.location.href = '/sh/switch/list';
        }, actionType);
    });
}
