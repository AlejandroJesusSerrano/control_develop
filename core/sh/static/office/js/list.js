$(document).ready(function(){
    $('#office_table').DataTable({
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
            {"data": "province"},
            {"data": "location"},
            {"data": "edifice"},
            {"data": "office"},
            {"data": "dependency"},
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [

            {
                targets: [5],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<button type="button" class="btn bg-custom-primary btn-detail" data-id="' + row.id +'"><i class="fas fa-search"></i></button> ';
                    buttons += '<a href="/sh/office/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/office/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons
                }
            }
        ],
        initComplete: function(settings, json){

        }
    });
});

function loadOfficeDetail(officeId) {
    $.ajax({
        url: '/sh/office/details/' + officeId + '/',
        type: 'GET',
        dataType: 'html',
        success: function(data){
            $('#officeDetailModal').remove();
            $('body').append(data);
            $('#officeDetailModal').modal('show');
            $('#officeDetailModal').on('hidden.bs.modal', function(){
                $(this).remove();
            });
        },
        error: function(xhr, status, error){
            console.log('Error al cargar la información de la oficina', error);
        }
    });
}

$(document).on('click', '.btn-detail', function(){
    let officeId = $(this).data('id');
    loadOfficeDetail(officeId);
});