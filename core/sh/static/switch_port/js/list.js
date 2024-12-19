$(document).ready(function(){

  $('#switch_port_table').DataTable({
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
      {"data": "rack"},
      {"data": "switch"},
      {"data": "port_id"},
      {"data": "obs"},
      {"data": null,  "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [5],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="/sh/switch_port/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/switch_port/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });
});