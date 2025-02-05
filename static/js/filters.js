$(document).ready(function() {

if ($('#id_province').length > 0) {
        $('select[name="province"]').on('change', function(){
            const province_id = $(this).val();
            updateLocationOptions(province_id);
        });
    }

if ($('#id_location').length > 0) {
    $('select[name="location"]').on('change', function(){
        const location_id = $(this).val();
        updateLocationReferedOptions(location_id);
        console.log('Localidad', location, 'seleccionada con el ID: ', location_id);

        if (location_id) {
            if ($('#id_edifice_ports').length > 0) {
                updateOptions('/sh/ajax/load_edifices/', {'location_id': location_id}, $('select[name="edifice_ports"]'), $('#id_edifice_ports').data('preselected'));
            }
            if ($('#id_loc_ports').length > 0) {
                updateOptions('/sh/ajax/load_loc/', {'location_id': location_id}, $('select[name="loc_ports"]'), $('#id_loc_ports').data('preselected'));
            }
            if ($('#id_office_ports').length > 0) {
                updateOptions('/sh/ajax/load_office/', {'location_id': location_id}, $('select[name="office_ports"]'), $('#id_office_ports').data('preselected'));
            }
            if ($('#id_rack_ports').length > 0) {
                updateOptions('/sh/ajax/load_rack/', {'location_id': location_id}, $('select[name="rack_ports"]'), $('#id_rack_ports').data('preselected'));
            }
            if ($('#id_switch_ports').length > 0) {
                updateOptions('/sh/ajax/load_switch/', {'location_id': location_id}, $('select[name="switch_ports"]'), $('#id_switch_ports').data('preselected'));
            }
            if ($('#id_patchera_ports').length > 0) {
                updateOptions('/sh/ajax/load_patchera/', {'location_id': location_id}, $('select[name="patchera_ports"]'), $('#id_patchera_ports').data('preselected'));
            }
            if ($('#id_wall_port_in').length > 0) {
                updateOptions('/sh/ajax/load_wall_port/', {'location_id': location_id}, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
            }
            if ($('#id_switch_port_in').length > 0) {
                updateOptions('/sh/ajax/load_switch_port/', {'location_id': location_id}, $('select[name="switch_port_in"]'), $('#id_switch_ports').data('preselected'));
            }
            if ($('#id_patch_port_in').length > 0) {
                updateOptions('/sh/ajax/load_patch_ports/', {'location_id': location_id}, $('select[name="patch_port_in"]'), $('#id_patchera_ports').data('preselected'));
            }

        } else {
            console.warn('No se ha seleccionado una localidad válida.');
            clearDependentFields(['#id_edifice_ports', '#id_loc_ports', '#id_office_ports', '#id_rack_ports', '#id_switch_ports', '#id_patchera_ports', '#id_wall_ports', '#id_switch_port_in', '#id_patch_port_in']);
        }
    });
}

if ($('#id_edifice').length > 0) {
    $('select[name="edifice"]').on('change', function(){
        const edifice_id = $(this).val();
        updateEdificeOptions(edifice_id);
    })
}

if ($('#id_dependency').length > 0) {
    $('select[name="dependency"]').on('change', function(){
        const dependency_id = $(this).val();
        updateDependencyOptions(dependency_id);
    })
}

if ($('#id_loc').length > 0) {
    $('select[name="loc"]').on('change', function(){
        const loc_id = $(this).val();
        updateLocOptions(loc_id);
    })
}

if ($('#id_office').length > 0) {
    $('#id_office').off('change');
    $('#id_office').on('change', function() {
        console.log("Evento change en #id_office (filters.js)");
        const office_id = $(this).val();
        console.log('office_id:', office_id);

        if (office_id) {
            $.ajax({
                url: '/sh/ajax/load_province_location/',
                type: 'POST',
                data: {
                    'office_id': office_id
                },
                dataType: 'json',
                success: function(data) {
                    console.log('Respuesta de ajax_load_province_location:', data);
                    if (!data.error) {
                        console.log('Provincia y Localidad cargadas:', data);

                        // Actualizar provincia
                        const provinceSelect = $('select[name="province"]');
                        provinceSelect.val(data.province_id).trigger('change.select2');

                        // Actualizar localidad
                        const locationSelect = $('select[name="location"]');
                        locationSelect.val(data.location_id).trigger('change.select2').trigger('change');

                        // Asegurarse de que la opción esté disponible antes de establecer el valor
                        console.log('Opciones disponibles en #id_office:', $('#id_office').find('option').map(function() {
                            return $(this).val();
                        }).get());

                        $('#id_office').val(office_id).trigger('change.select2');
                        $('#id_office').select2('destroy').select2({ theme: 'bootstrap' });
                        console.log('Valor establecido en #id_office:', $('#id_office').val());
                    } else {
                        console.error('Error: ', data.error);
                    }
                },
                    error: function(xhr, status, error) {
                    console.error('AJAX Error: ', status, error);
                    }
                });
            }
        });
    }
});

function updateLocationOptions(province_id) {
    if (province_id) {
        if ($('#id_location').length > 0) {
            updateOptions('/sh/ajax/load_location/', {
                'province_id': province_id,
            }, $('select[name="location"]'), $('#id_location').data('preselected'));
        }

        if ($('#id_dependency').length > 0) {
            updateOptions('/sh/ajax/load_dependency/', {
            'province_id': province_id,
            }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
        }

        if ($('#id_edifice').length > 0) {
            updateOptions('/sh/ajax/load_edifices/', {
                'province_id': province_id,
            }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
        }

        if ($('#id_loc').length > 0) {
            updateOptions('/sh/ajax/load_loc/', {
                'province_id': province_id,
            }, $('select[name="loc"]'), $('#id_loc').data('preselected'));
        }

        if ($('#id_office').length > 0) {
            updateOptions('/sh/ajax/load_office/', {
                'province_id': province_id,
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        }

        if ($('#id_employee').length > 0) {
            updateOptions('/sh/ajax/load_employee/', {
                'province_id': province_id,
            }, $('select[name="employee"]'), $('#id_employee').data('preselected'));
        }

        if ($('#id_rack').length > 0) {
            updateOptions('/sh/ajax/load_rack/', {
                'province_id': province_id,
            }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
        }

    } else {
        clearDependentFields(['#id_location', '#id_dependency', '#id_edifice', '#id_loc', '#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
    }
};

function updateLocationReferedOptions(location_id) {
    if (location_id) {
        if ($('#id_dependency').length > 0) {
            updateOptions('/sh/ajax/load_dependency/', {
                'location_id': location_id,
            }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
        }

        if ($('#id_edifice').length > 0) {
            updateOptions('/sh/ajax/load_edifices/', {
                'location_id': location_id,
            }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
        }

        if ($('#id_loc').length > 0) {
            updateOptions('/sh/ajax/load_loc/', {
                'location_id': location_id,
            }, $('select[name="loc"]'), $('#id_loc').data('preselected'));
        }

        if ($('#id_office').length > 0) {
            updateOptions('/sh/ajax/load_office/', {
                'location_id': location_id,
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        }


        if ($('#id_rack').length > 0) {
            updateOptions('/sh/ajax/load_rack/', {
                'location_id': location_id,
            }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
        }

    } else {
        clearDependentFields(['#id_dependency', '#id_edifice', '#id_loc', '#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
    }
};


function updateDependencyOptions(dependency_id) {
    if (dependency_id) {
        if ($('#id_office').length > 0) {
            updateOptions('/sh/ajax/load_office/', {
                'dependency_id': dependency_id,
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        }


        if ($('#id_rack').length > 0) {
            updateOptions('/sh/ajax/load_rack/', {
                'dependency_id': dependency_id,
            } , $('select[name="rack"]'), $('#id_rack').data('preselected'));
        }

    } else {
        clearDependentFields(['#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
    }
};

function updateEdificeOptions(edifice_id) {
    if (edifice_id) {
        if ($('#id_loc').length > 0) {
            updateOptions('/sh/ajax/load_loc/', {
                'edifice_id': edifice_id
            }, $('select[name="loc"]'), $('#id_loc').data('preselected'));
        }

        if ($('#id_office').length > 0) {
            updateOptions('/sh/ajax/load_office/', {
                'edifice_id': edifice_id,
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        }

        if ($('#id_wall_port_in').length > 0) {
            updateOptions('/sh/ajax/load_wall_port/', {
                'edifice_id': edifice_id,
            }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
        }

        if ($('#id_rack').length > 0) {
            updateOptions('/sh/ajax/load_rack/', {
                'edifice_id': edifice_id,
            }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
        }

    } else {
        clearDependentFields(['#id_loc', '#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
    }
};

function updateLocOptions(loc_id) {
    if (loc_id) {
        if ($('#id_office').length > 0) {
            updateOptions('/sh/ajax/load_office/', {
                'loc_id': loc_id
            }, $('select[name="office"]'), $('#id_office').data('preselected'));
        }

        if ($('#id_wall_port_in').length > 0) {
            updateOptions('/sh/ajax/load_wall_port/', {
                'loc_id': loc_id,
            }, $('select[name="wall_port_in"]'), $('#id_wall_port_in').data('preselected'));
        }

        if ($('#id_rack').length > 0) {
            updateOptions('/sh/ajax/load_rack/', {
                'loc_id': loc_id,
            }, $('select[name="rack"]'), $('#id_rack').data('preselected'));
        }

    } else {
        clearDependentFields(['#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
    }
};

function updateRackOptions(rack_id) {
    if (rack_id) {
        if ($('#id_switch').length > 0) {
            updateOptions('/sh/ajax/load_switch/', {
                'rack_id': rack_id,
            }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
        }

        if ($('#id_patchera').length > 0) {
            updateOptions('/sh/ajax/load_patchera/', {
                'rack_id': rack_id,
            }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
        }
    } else {
        clearDependentFields(['#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
    }
};
