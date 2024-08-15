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
      dataSrc: "data"
    },
    columns: [
      {"data": "id"},
      {"data": "type"},
      {"data": "brand"},
      {"data": "model"},
      {"data": "ip"},
      {"data": "w_port"},
      {"data": "s_port"},
      {"data": "office"},
      {
        "data": "employees",
        "render": function (data, type, row){
          const employeeNames = data.map(employee => `${employee.employee_last_name} ${employee.employee_name}`);
          return employeeNames.join(', ');
        }
      },
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [9],
        class: 'text-center align-middle',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="#" type="button" class="btn btn-primary"><i class="fas fa-search"></i></a> ';
          buttons += '<a href="/sh/device/edit/'+row.id+'/" type="button" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/device/delete/'+row.id+'/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
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