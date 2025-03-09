
$(document).ready(function() {

    $('#move_type_table').DataTable({
        responsive: true,
        autoWidth:false,
        destroy: true,
        deferRender:false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "move" },
            { "data": "details" },
            { "data": "" },
        ],
        columnDefs: [
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<a href="/sh/move_type/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/move_type/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;
                },
            },
        ],
        initComplete: function(settings, json) {

        }
    });
});