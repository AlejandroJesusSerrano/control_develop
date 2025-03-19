$(document).ready(function(){
    $('#employee_table').DataTable({
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
            {"data": "employee_full_name"},
            {"data": "cuil"},
            {"data": "user_pc"},
            {"data": "status"},
            {"data": "office"},
            {"data": "dependency"},
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [6],
                class: 'text-center align-middle',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<button type="button" class="btn bg-custom-primary btn-detail" data-id="' + row.id + '"><i class="fas fa-search"></i></button> ';
                    buttons += '<a href="/sh/employee/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/employee/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
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

function loadEmployeeDetail(employeeId) {
    $.ajax({
        url: '/sh/employee/details/' + employeeId + '/',
        type: 'GET',
        dataType: 'html',
        success: function(data){
            $('#employeeDetailModel').remove();
            $('body').append(data);
            $('#employeeDetailModal').modal('show');
            $('#employeeDetailModal').on('hidden.bs.modal', function () {
                $(this).remove();
            });
        },
        error: function(xhr, status, error){
            console.log('Error al cargar la vista de detalle de empleado', error);
        }
    });
}

$(document).on('click', '.btn-detail', function(){
    let employeeId = $(this).data('id');
    loadEmployeeDetail(employeeId);
});