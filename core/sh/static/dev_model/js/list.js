$(document).ready(function(){

    $('#dev_model_table').DataTable({
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
            {"data": "dev_model"},
            {"data": "dev_type"},
            {"data": "brand"},
            {
                "data": "image",
                "render": function(data, type, row){
                    return '<img src="' + data + '" class="img-thumbnail" style="max-width:100px;"/>';
                }
            },
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [4],
                class: 'text-center align-middle',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<button type="button" class="btn bg-custom-primary btn-detail" data-id="' + row.id + '"><i class="fas fa-search"></i></button> ';
                    buttons += '<a href="/sh/dev_model/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/dev_model/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons
                }
            },
            {
                targets: '_all',
                class: 'align-middle'
            }
        ],
        initComplete: function(settings, json){

        }
    });
});

function loadDevModelDetail(devModelId) {
    $.ajax({
        url: '/sh/dev_model/details/' + devModelId + '/',
        type: 'GET',
        dataType: 'html',
        success: function(data){
            $('#devModelDetailModal').remove();
            $('body').append(data);
            $('#devModelDetailModal').modal('show');
            $('#devModelDetailModal').on('hidden.bs.modal', function(){
                $(this).remove();
            });
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log('Error al cargar la información del modelo de dispositivo', error);
        }
    });
}

$(document).on('click', '.btn-detail', function(){
    let devModelId = $(this).data('id');
    loadDevModelDetail(devModelId);
});
