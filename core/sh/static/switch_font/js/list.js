$(document).ready(function(){

    $('#switch_font_table').DataTable({
        responsive: true,
        autowidth: false,
        destroy: true,
        deferRender:false,
        ajax: {
            url:window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "font"},
            {"data": "switch"},
            {"data": "rack"},
            {"data": "status"},
            {"data": "send"},
            {"data": "reception"},
            {"data": null,  "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<a href="/sh/switch_font/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/switch_font/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons
                }
            }
        ],
        initComplete: function(settings, json){

        }
    });
});