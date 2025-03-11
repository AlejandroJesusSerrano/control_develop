$(document).ready(function(){

    $('#rack_table').DataTable({
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
            {"data": "rack"},
            {"data": "details"},
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<a href="/sh/rack/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/rack/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons
                }
            }
        ],
        initComplete: function(settings, json){

        }
    });
});