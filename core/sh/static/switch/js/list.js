$(document).ready(function(){

    $('#switch_table').DataTable({
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
            {"data": "brand"},
            {"data": "model"},
            {"data": "ports_q"},
            {"data": "conection_in"},
            {"data": "office"},
            {"data": "rack"},
            {"data": "switch_rack_pos"},
            {"data": null, "defaultContent": ""},
        ],
        columnDefs: [
            {
                targets: [7],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    let buttons = '<button type="button" class="btn bg-custom-primary btn-detail" data-id="' + row.id + '"><i class="fas fa-search"></i></button> ';
                    buttons += '<a href="/sh/switch/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sh/switch/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
                    return buttons
                }
            }
        ],
        initComplete: function(settings, json){

        }
    });
});

function loadSwitchDetail(switchId){
    $.ajax({
        url: '/sh/switch/detail/' +switchId+ '/',
        type: 'GET',
        dataType: 'html',
        success: function(data){
            $('#switchDetailModal').remove();
            $('body').append(data);
            $('#switchDetailModal').modal('show');
            $('#switchDetailModal').on('hidden.bs.modal', function(){
                $(this).remove();
            });
        },
        error: function(xhr, status, error){
            console.log('Error al cargar los detalles del switch:', error);
        }
    });
}

$(document).on('click', '.btn-detail', function(){
    let switchId = $(this).data('id');
    loadSwitchDetail(switchId);
});