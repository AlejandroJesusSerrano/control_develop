$(document).ready(function(){

  $('#patch_port_table').DataTable({
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
      {"data": "patch"},
      {"data": "port"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [4],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="/sh/patch_port/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/patch_port/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });
});