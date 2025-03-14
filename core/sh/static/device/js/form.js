$(document).ready(function() {
    $('.select2').select2({
        theme: 'bootstrap',
    });

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

    if ($('#id_switch_ports').length > 0) {
        $('select[name="switch_ports"]').on('change', function() {
            const switch_ports_id = $(this).val();
            if (switch_ports_id) {
                updateOptions('/sh/ajax/load_switch_port/', {
                    'switch_id': switch_ports_id
                }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));

                $('select[name="patchera_ports"]').val(null).trigger('change');
                $('select[name="patch_port_in"]').val(null).trigger('change');
                $('select[name="patch_port_in"]').closest('.form-group').hide();
            } else {
                $('select[name="patch_port_in"]').closest('.form-group').show();
            }
        });
    }

    if ($('#id_patchera_ports').length > 0) {
        $('select[name="patchera_ports"]').on('change', function() {
            const patchera_id = $(this).val();
            if (patchera_id){
                updateOptions('/sh/ajax/load_patch_ports/', {
                    'patchera_id': patchera_id
                }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));

                $('select[name="switch_ports"]').val(null).trigger('change');
                $('select[name="switch_port_in"]').val(null).trigger('change');
                $('select[name="switch_port_in"]').closest('.form-group').hide();
            } else {
                $('select[name="switch_port_in"]').closest('.form-group').show();
            }
        });
    }



    $('select[name="dev_type"]').on('change', function() {
        const dev_type = $(this).val();
        updateBrandOptions(dev_type);
        updateModelOptions(dev_type);
    });

    if ($('#id_brand').length > 0) {
        $('select[name="brand"]').on('change', function() {
            const brand_id = $(this).val();
            const dev_type = $('select[name="dev_type"]').val() || '';
            updateModelOptions(dev_type, brand_id);
        });
    }


    $('#toggle-device-filters').on('click', function(e) {
        e.preventDefault();
        const filterLocCards = $('#filter-device-cards')
        filterLocCards.toggleClass('d-none')

        $(this).toggleClass('active btn-primary btn-secondary')

        if (filterLocCards.hasClass('d-none')) {
            $(this).html('Filtros para Modelos de Dispositivos <i class="fas fa-search"></i>');
        } else {
            $(this).html('Ocultar Filtros <i class = "fas fa-times"></i>')
        }
    });


    $('#toggle-office-filters').on('click', function(e) {
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

    $('#toggle-ports-filters').on('click', function(e) {
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

    $('#dev_model_popup_add').on('click', function() {
        let url = modelAddUrl + '?popup=1&context=device';
        let popup = window.open(url, 'Agregar Modelo de Dispositivo', 'width=800, height=500');
        popup.focus();
    });

    $('#office_popup_add').on('click', function() {
        let url = officeAddUrl + '?popup=1';
        let popup = window.open(url, 'Agregar Oficina', 'width=800, height=750');
        popup.focus();
    });

    $('#employee_popup_add').on('click', function() {
        let url = employeeAddUrl + '?popup=1';
        let popup = window.open(url, 'Agregar Empleado', 'width=800, height=700');
        popup.focus();
    });

    $('#wall_port_popup_add').on('click', function() {
        let url = wallPortAddUrl + '?popup=1';
        let popup = window.open(url, 'Agregar Puerto de Pared', 'width=800, height=825');
        popup.focus();
    });

    $('#switch_port_popup_add').on('click', function() {
        let url = switchPortAddUrl + '?popup=1';
        let popup = window.open(url, 'Agregar Puerto de Switch', 'width=800, height=650');
        popup.focus();
    });

    $('#patch_port_popup_add').on('click', function() {
        let url = patchPortAddUrl + '?popup=1';
        let popup = window.open(url, 'Agregar Puerto de Patchera', 'width=800, height=400');
        popup.focus();
    });

    window.addEventListener('message', function(event) {
        if (event.data.type === 'dev_modelAdded') {
            let dev_modelId = event.data.id;
            let dev_modelName = event.data.name;
            let select = $('#id_dev_model');
            let option = new Option(dev_modelName, dev_modelId, true, true);
            select.append(option).val(dev_modelId).trigger('change');
        }

        if (event.data.type === 'officeAdded') {
            let officeId = event.data.id;
            let officeName = event.data.name;
            let select = $('#id_office');
            let option = new Option(officeName, officeId, true, true);
            select.append(option).val(officeId).trigger('change');
        }

        if (event.data.type === 'employeeAdded') {
            let employeeId = event.data.id;
            let employeeName = event.data.name;
            let select = $('#id_employee');
            let option = new Option(employeeName, employeeId, true, true);
            select.append(option).val(employeeId).trigger('change');
        }

        if (event.data.type === 'wall_portAdded') {
            let wall_portId = event.data.id;
            let wall_portName = event.data.name;
            let select = $('#id_wall_port');
            let option = new Option(wall_portName, wall_portId, true, true);
            select.append(option).val(wall_portId).trigger('change');
        }

        if (event.data.type === 'switch_portAdded') {
            let switch_portId = event.data.id;
            let switch_portName = event.data.name;
            let select = $('#id_switch_port');
            let option = new Option(switch_portName, switch_portId, true, true);
            select.append(option).val(switch_portId).trigger('change');
        }

        if (event.data.type === 'patch_portAdded') {
            let patch_portId = event.data.id;
            let patch_portName = event.data.name;
            let select = $('#id_patch_port');
            let option = new Option(patch_portName, patch_portId, true, true);
            select.append(option).val(patch_portId).trigger('change');
        }
    });




    initializeFormSubmission('#myform', 'edit');

});

function updateEdificePortsFromLocation(location_id) {
    console.log('updateEdificePortsFromLocation llamada con location_id: ', location_id);
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
    if (office_ports_id) {
        if ($('#id_rack_ports').length > 0) {
            updateOptions('/sh/ajax/load_rack/', {
                'office_id': office_ports_id
            }, $('select[name="rack_ports"]'), $('#id_rack_ports').data('preselected'));
        }
    } else {
        clearDependentFields(['#id_rack_ports', '#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in', '#id_wall_port_in']);
    }
}

function updateRackPortsOptions(rack_ports_id) {
    if (rack_ports_id) {
        if ($('#id_switch_ports').length > 0) {
            updateOptions('/sh/ajax/load_switch/', {
                'rack_id': rack_ports_id
            }, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
        }
    } else {
        clearDependentFields(['#id_switch_ports', '#id_switch_port_in', '#id_patchera_ports', '#id_patch_port_in']);
    }
}

function updateSwitchPortsOptions(switch_id) {
    updateOptions('/sh/ajax/load_switch_port/', {
        'switch_id': switch_id
    }, $('select[name="switch_port_in"]'), $('#id_switch_port_in').data('preselected'));
}

function updatePatcheraPortsOptions(patchera_id) {
    updateOptions('/sh/ajax/load_patch_ports/', {
        'patchera_id': patchera_id
    }, $('select[name="patch_port_in"]'), $('#id_patch_port_in').data('preselected'));
}


function updateBrandOptions(dev_type) {
    updateOptions('/sh/ajax/load_brand/', {
        'usage': 'device',
        'dev_type_name': dev_type
    }, $('select[name="brand"]'));
}

function updateModelOptions(dev_type, brand_id) {
    updateOptions('/sh/ajax/load_model/', {
        'usage': 'device',
        'dev_type_name': dev_type,
        'brand_id': brand_id
    }, $('select[name="dev_model"]'));
}

function initializeFormSubmission(formSelector, actionType) {
    $(formSelector).on('submit', function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        submit_with_ajax($(this).attr('action'), formData, function() {
            console.log('Formulario enviado y procesado con éxito');
            window.location.href = '/sh/device/list';
        }, actionType);
    });
}