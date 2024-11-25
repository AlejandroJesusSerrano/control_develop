$(document).ready(function(){

  $('#wall_port_table').DataTable({
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
      {"data": "office"},
      {"data": "wall_port"},
      {"data": "patch_port_in"},
      {"data": "switch_port_in"},
      {"data": "details"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: [-1],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="/sh/wall_port/edit/'+row.id+'/" type="button" class="btn btn-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/wall_port/delete/'+row.id+'/" type="button" class="btn btn-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      },
      {
        // Renderizado para columna de switch
        targets: [4],
        render: function(data, type, row) {
            return data || '<span class="badge bg-secondary">Sin conexión a switch</span>';
        }
      },
      {
        // Renderizado para columna de patchera
        targets: [3],
        render: function(data, type, row) {
            return data || '<span class="badge bg-secondary">Sin conexión a patchera</span>';
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });
});