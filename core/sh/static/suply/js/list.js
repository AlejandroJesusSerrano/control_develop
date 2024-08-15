$(document).ready(function(){
  $('#suply_table').DataTable({
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
      {"data": "suply_type"},
      {"data": "brand"},
      {"data": "dev_model"},
      {"data": "serial_suply"},
      {"data": "date_in"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [6],
        class: 'text-center align-middle',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="/sh/suply/edit/'+row.id+'/" type="button" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/suply/delete/'+row.id+'/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
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