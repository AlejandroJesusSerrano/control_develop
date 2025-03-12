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

// $(document).ready(function() {

// if ($('#id_province').length > 0) {
//         $('select[name="province"]').on('change', function(){
//             const province_id = $(this).val();
//             updateLocationOptions(province_id);
//         });
//     }

// if ($('#id_location').length > 0) {
//     $('select[name="location"]').on('change', function(){
//         const location_id = $(this).val();
//         updateLocationReferedOptions(location_id);
//         console.log('Localidad', location, 'seleccionada con el ID: ', location_id);

//         if (location_id) {
//             if ($('#id_edifice_ports').length > 0) {
//                 updateOptions('/sh/ajax/load_edifices/', {'location_id': location_id}, $('select[name="edifice_ports"]'), $('#id_edifice_ports').data('preselected'));
//             }

//             if ($('#id_edifice').length > 0) {
//                 updateOptions('/sh/ajax/load_edifices/', {'location_id': location_id}, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
//             }

//             if ($('#id_dependency').length > 0) {
//                 updateOptions('/sh/ajax/load_dependency/', {'location_id': location_id}, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
//             }

//         } else {
//             console.warn('No se ha seleccionado una localidad válida.');
//             clearDependentFields(['#id_edifice_ports', '#id_loc_ports', '#id_office_ports', '#id_rack_ports', '#id_switch_ports', '#id_patchera_ports', '#id_wall_ports', '#id_switch_port_in', '#id_patch_port_in']);
//         }
//     });
// }

// if ($('#id_edifice').length > 0) {
//     $('select[name="edifice"]').on('change', function(){
//         const edifice_id = $(this).val();
//         updateEdificeOptions(edifice_id);
//     })
// }

// if ($('#id_dependency').length > 0) {
//     $('select[name="dependency"]').on('change', function(){
//         const dependency_id = $(this).val();
//         updateDependencyOptions(dependency_id);
//     })
// }

// if ($('#id_loc').length > 0) {
//     $('select[name="loc"]').on('change', function(){
//         const loc_id = $(this).val();
//         updateLocOptions(loc_id);
//     })
// }


// function updateLocationOptions(province_id) {
//     if (province_id) {
//         if ($('#id_location').length > 0) {
//             updateOptions('/sh/ajax/load_location/', {
//                 'province_id': province_id,
//             }, $('select[name="location"]'), $('#id_location').data('preselected'));
//         }

//     } else {
//         clearDependentFields(['#id_location', '#id_dependency', '#id_edifice', '#id_loc', '#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
//     }
// };

// function updateLocationReferedOptions(location_id) {
//     if (location_id) {

//         if ($('#id_edifice_ports').length > 0) {
//             updateOptions('/sh/ajax/load_edifices/', {
//                 'location_id': location_id,
//             }, $('select[name="edifice_ports"]'), $('#id_edifice_ports').data('preselected'));
//         }

//         if ($('#id_dependency').length > 0) {
//             updateOptions('/sh/ajax/load_dependency/', {
//                 'location_id': location_id,
//             }, $('select[name="dependency"]'), $('#id_dependency').data('preselected'));
//         }

//         if ($('#id_edifice').length > 0) {
//             updateOptions('/sh/ajax/load_edifices/', {
//                 'location_id': location_id,
//             }, $('select[name="edifice"]'), $('#id_edifice').data('preselected'));
//         }

//     } else {
//         clearDependentFields(['#id_dependency', '#id_edifice', '#id_loc', '#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
//     }
// };


// function updateDependencyOptions(dependency_id) {
//     if (dependency_id) {
//         if ($('#id_office').length > 0) {
//             updateOptions('/sh/ajax/load_office/', {
//                 'dependency_id': dependency_id,
//             }, $('select[name="office"]'), $('#id_office').data('preselected'));
//         }


//     } else {
//         clearDependentFields(['#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
//     }
// };

// function updateEdificeOptions(edifice_id) {
//     if (edifice_id) {
//         if ($('#id_loc').length > 0) {
//             updateOptions('/sh/ajax/load_loc/', {
//                 'edifice_id': edifice_id
//             }, $('select[name="loc"]'), $('#id_loc').data('preselected'));
//         }

//     } else {
//         clearDependentFields(['#id_loc', '#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
//     }
// };

// function updateLocOptions(loc_id) {
//     if (loc_id) {
//         if ($('#id_office').length > 0) {
//             updateOptions('/sh/ajax/load_office/', {
//                 'loc_id': loc_id
//             }, $('select[name="office"]'), $('#id_office').data('preselected'));
//         }

//     } else {
//         clearDependentFields(['#id_wall_port_in', '#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
//     }
// };

// function updateRackOptions(rack_id) {
//     if (rack_id) {
//         if ($('#id_switch').length > 0) {
//             updateOptions('/sh/ajax/load_switch/', {
//                 'rack_id': rack_id,
//             }, $('select[name="switch"]'), $('#id_switch').data('preselected'));
//         }

//         if ($('#id_patchera').length > 0) {
//             updateOptions('/sh/ajax/load_patchera/', {
//                 'rack_id': rack_id,
//             }, $('select[name="patchera"]'), $('#id_patchera').data('preselected'));
//         }
//     } else {
//         clearDependentFields(['#id_switch', '#id_switch_port_in', '#id_patchera', '#id_patch_port_in'])
//     }
// }
// });