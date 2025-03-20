$(document).ready(function(){

    $('#device_table').DataTable({
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
            {"data": "type"},
            {"data": "brand"},
            {"data": "model"},
            {"data": "ip"},
            {"data": "office"},
            {
                "data": "employee",
                "render": function(data, type, row){
                    if (Array.isArray(data)){
                        return data.join('<br>');
                    } else {
                        return data;
                    }
                }
            },
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [6],
                class: 'text-center align-middle',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<button type="button" class="btn bg-custom-primary btn-detail" data-id="' + row.id + '"><i class="fas fa-search"></i></button> ';
                    buttons += '<a href="/sh/device/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/device/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
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

function loadDeviceDetail(deviceId) {
    $.ajax({
        url: '/sh/device/details/' + deviceId + '/',
        type: 'GET',
        dataType: 'html',
        success: function(data) {
            $('#deviceDetailModal').remove();
            $('body').append(data);
            $('#deviceDetailModal').modal('show');
            $('#deviceDetailModal').on('hidden.bs.modal', function() {
                $(this).remove();
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el detalle del dispositivo: ', error);
        }
    });
}

$(document).on('click', '.btn-detail', function(){
    let deviceId = $(this).data('id');
    loadDeviceDetail(deviceId);
});