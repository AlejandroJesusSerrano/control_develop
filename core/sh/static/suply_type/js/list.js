
$(document).ready(function() {

    $('#suply_type_table').DataTable({
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
            { "data": "suply_type" },
            { "data": null, "defaultContent": "" },
        ],
        columnDefs: [
            {
                targets: [1],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<a href="/sh/suply_type/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/suply_type/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons;
                },
            },
        ],
        initComplete: function(settings, json) {

        }
    });
});