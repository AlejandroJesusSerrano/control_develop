$(document).ready(function(){

  $('#dev_status_table').DataTable({
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
      {"data": "dev_status"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [2],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="/sh/dev_status/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/dev_status/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });
});