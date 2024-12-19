$(document).ready(function(){

  $('#dev_model_table').DataTable({
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
      {
        "data": "image",
        "render": function(data, type, row){
          return '<img src="' + data + '" class="img-thumbnail" style="max-width:100px;"/>';
        }
      },
      {"data": "dev_model"},
      {"data": "dev_type"},
      {"data": "brand"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [5],
        class: 'text-center align-middle',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="#" type="button" class="btn btn-primary"><i class="fas fa-search"></i></a> ';
          buttons += '<a href="/sh/dev_model/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/dev_model/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
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