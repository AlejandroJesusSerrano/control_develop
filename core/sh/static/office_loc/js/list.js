$(document).ready(function(){
  $('#office_loc_table').DataTable({
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
      {"data": "location"},
      {"data": "edifice"},
      {"data": "floor"},
      {"data": "wing"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [5],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
<<<<<<< HEAD
          let buttons = '<a href="#" type="button" class="btn btn-primary"><i class="fas fa-search"></i></a> ';
          buttons += '<a href="/sh/office_loc/edit/'+row.id+'/" type="button" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
=======
          let buttons = '<a href="/sh/office_loc/edit/'+row.id+'/" type="button" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
>>>>>>> d0c807020e7c9a0e7ff6bbdc6c32a67308d211bc
          buttons += '<a href="/sh/office_loc/delete/'+row.id+'/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });
});