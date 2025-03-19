$(document).ready(function(){

    $('#movement_table').DataTable({
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
            {"data": "equipment"},
            {"data": "office"},
            {"data": "employee"},
            {"data": "move"},
            {"data": "techs"},
            {"data": "date"},
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [6],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<button type="button" class="btn bg-custom-primary btn-detail" data-id="' + row.id + '"><i class="fas fa-search"></i></button> ';
                    buttons += '<a href="/sh/move/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/move/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons
                }
            }
        ],
        initComplete: function(settings, json){
        }
    });
});

function loadMovementDetail(movementId) {
    $.ajax({
        url: '/sh/move/details/' + movementId + '/',
        type: 'GET',
        dataType: 'html',
        success: function(data) {
            $('#movementDetailModal').remove();
            $('body').append(data);
            $('#movementDetailModal').modal('show');
            $('#movementDetailModal').on('hidden.bs.modal', function() {
                $(this).remove();
            });
        },
        error: function(xhr, status, error) {
            console.error('Error al cargar el detalle del movimiento: ', error);
        }
    });
}

$(document).on('click', '.btn-detail', function(){
    let movementId = $(this).data('id');
    loadMovementDetail(movementId);
});
