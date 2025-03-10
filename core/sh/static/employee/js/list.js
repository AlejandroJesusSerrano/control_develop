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
      {"data": "user_pc"},
      {"data": "status"},
      {"data": "office"},
      {
        "data": "avatar",
        "render": function(data, type, row){
          return '<img src="' + data + '" class="img-thumbnail" style="max-width:100px;"/>';
        },
      },
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [5],
        class: 'text-center align-middle',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="#" type="button" class="btn btn-primary"><i class="fas fa-search"></i></a> ';
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