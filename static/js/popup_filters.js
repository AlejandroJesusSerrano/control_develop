function toggleFields(switchSelector, patcheraSelector) {

    function updateFields() {
        let wallPortValue = $(wallPortSelector).val();
        let switchValue = $(switchSelector).val();
        let patcheraValue = $(patcheraSelector).val();

        if (wallPortValue) {
            $(switchSelector).prop('disabled', true);
            $(patcheraSelector).prop('disabled', true);
        } else {
            $(switchSelector).prop('disabled', false);
            $(patcheraSelector).prop('disabled', false);
        }

        if (switchValue) {
            $(patcheraSelector).prop('disabled', true);
            $(wallPortValue).prop('disabled', true);
        } else {
            $(patcheraSelector).prop('disabled', false);
            $(wallPortValue).prop('disabled', false);
        }

        if (patcheraValue) {
            $(switchSelector).prop('disabled', true);
            $(wallPortValue).prop('disabled', true);
        } else {
            $(switchSelector).prop('disabled', false);
            $(wallPortValue).prop('disabled', false);
        }
    }

    updateFields();
    $(switchSelector).on('change', updateFields);
    $(patcheraSelector).on('change', updateFields);
    $(wallPortSelector).on('change', updateFields);
};

function initPopupFilters(officeSelector, switchSelector, patcheraSelector, switchPortSelector, patcheraPortSelector, wallPortSelector, rackSelector, urls, enableToggle) {
    $(officeSelector).on('change', function () {
        let office_id = $(this).val();
        if (office_id) {

            if (switchSelector) {

                $.ajax({
                    url: urls.load_switches,
                    data: {
                        'office_id': office_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(switchSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(switchSelector).append(new Option(item.name, item.id));
                        });
                        $(switchSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar switches: ', error)
                    }
                });
            }

            if (patcheraSelector) {

                $.ajax({
                    url: urls.load_patcheras,
                    data: {
                        'office_id': office_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(patcheraSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(patcheraSelector).append(new Option(item.name, item.id));
                        });
                        $(patcheraSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar patcheras: ', error)
                    }
                });
            }

            if (wallPortSelector) {

                $.ajax({
                    url: urls.load_wall_ports,
                    data: {
                        'office_id': office_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(wallPortSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(wallPortSelector).append(new Option(item.name, item.id));
                        });
                        $(wallPortSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar bocas de pared: ', error)
                    }
                });
            }

            if (rackSelector) {

                $.ajax({
                    url: urls.load_racks,
                    data: {
                        'office_id': office_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(rackSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(rackSelector).append(new Option(item.name, item.id));
                        });
                        $(rackSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar racks: ', error)
                    }
                });
            }
        } else {
            if (switchSelector) $(switchSelector).empty().trigger('change');
            if (patcheraSelector) $(patcheraSelector).empty().trigger('change');
            if (wallPortSelector) $(wallPortSelector).empty().trigger('change');
            if (rackSelector) $(rackSelector).empty().trigger('change');
        }
    });

    if (rackSelector && switchSelector) {
        $(rackSelector).on('change', function () {
            let rack_id = $(this).val();
            if (rack_id) {
                $.ajax({
                    url: urls.load_switches,
                    data: {
                        'rack_id': rack_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(switchSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(switchSelector).append(new Option(item.name, item.id));
                        });
                        $(switchSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar switches: ', error)
                    }
                });
            } else {
                $(switchSelector).empty().trigger('change');
            }
        });
    }

    if (rackSelector && patcheraSelector) {
        $(rackSelector).on('change', function () {
            let rack_id = $(this).val();
            if (rack_id) {
                $.ajax({
                    url: urls.load_patcheras,
                    data: {
                        'rack_id': rack_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(patcheraSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(patcheraSelector).append(new Option(item.name, item.id));
                        });
                        $(patcheraSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar patcheras: ', error)
                    }
                });
            } else {
                $(patcheraSelector).empty().trigger('change');
            }
        });
    }

    if (switchSelector && switchPortSelector) {

        $(switchSelector).on('change', function () {
            let switch_id = $(this).val();
            if (switch_id) {
                $.ajax({
                    url: urls.load_switch_ports,
                    data: {
                        'switch_id': switch_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(switchPortSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(switchPortSelector).append(new Option(item.name, item.id));
                        });
                        $(switchPortSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar puertos del switch: ', error)
                    }
                });
            } else {
                $(switchPortSelector).empty();
            }
        });
    }

    if(patcheraSelector && patcheraPortSelector) {

        $(patcheraSelector).on('change', function () {
            let patchera_id = $(this).val();
            if (patchera_id) {
                $.ajax({
                    url: urls.load_patch_ports,
                    data: {
                        'patchera_id': patchera_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        $(patcheraPortSelector).empty().append(new Option('---------', '', true, true));
                        $.each(data, function (index, item) {
                            $(patcheraPortSelector).append(new Option(item.name, item.id));
                        });
                        $(patcheraPortSelector).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error('Error al cargar puertos de la patchera: ', error)
                    }
                });
            } else {
                $(patcheraPortSelector).empty();
            }
        });
    }
    if (enableToggle) {
        toggleFields(switchSelector, patcheraSelector);
    }

}

