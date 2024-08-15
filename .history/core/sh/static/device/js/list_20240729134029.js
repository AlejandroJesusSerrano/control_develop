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
      {"data": "id"},
      {"data": "dev_model"},
      {"data": "dev_type"},
      {"data": "ip"},
      {"data": "dev_net_name"},
      {"data": "serial_number"},
      {"data": "dev_status"},
      {"data": "office"},
      {"data": "wall_port"},
      {"data": "switch_in"},
      {"data": "employee"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [11],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="#" type="button" class="btn btn-primary"><i class="fas fa-search"></i></a> ';
          buttons += '<a href="/sh/device/edit/'+row.id+'/" type="button" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/device/delete/'+row.id+'/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });
});