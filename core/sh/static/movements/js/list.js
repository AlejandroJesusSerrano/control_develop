$(document).ready(function(){

  $('#movement_table').DataTable({
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
      {"data": "device"},
      {"data": "office"},
      {"data": "employee"},
      {"data": "move"},
      {"data": "techs"},
      {"data": "date"},
      {"data": "suply"},
      {"data": null, "defaultContent": ""},
    ],
    columnDefs: [
      {
        targets: 1,
        render: function(data, type, row){
          return row.device || row.switch;
        }
      },
      {

        targets: [8],
        class: 'text-center',
        orderable: false,
        render: function(data, type, row){
          let buttons = '<a href="#" type="button" class="btn btn-primary btn-detail" data-id="' + row.id + '"><i class="fas fa-search"></i></a> ';
          buttons += '<a href="/sh/move/edit/'+row.id+'/" type="button" class="btn bg-custom-warning"><i class="fas fa-edit"></i></a> ';
          buttons += '<a href="/sh/move/delete/'+row.id+'/" type="button" class="btn bg-custom-danger"><i class="fas fa-trash-alt"></i></a> ';
          return buttons
        }
      }
    ],
    initComplete: function(settings, json){

    }
  });

  $(document).on('click', '.btn-detail', function(e){
    e.preventDefault();
    const movementId = $(this).attr('data-id');
    loadMovementDetail(movementId);
  });

  function loadMovementDetail(movementId){
    $.ajax({
      url: window.location.pathname,
      type: 'POST',
      data: {
        'action': 'get-details',
        'id': movementId
      },
      dataType: 'json',
      success: function(data){
        if(data){
          $('#detail-id').text(data.id);
          $('#detail-device').text(data.device) || (data.switch);
          $('#detail-office').text(data.office);
          $('#detail-employee').text(data.employee);
          $('#detail-move').text(data.move);
          $('#detail-techs').text(data.techs);
          $('#detail-date').text(data.date);
          $('#detail-suply').text(data.suply);
          $('#detail-detail').text(data.detail);

          $('#movementDetailModal').modal('show');
        }
      },
      error: function(xhr, status, error){
        console.error('Error al intentar cargar el detalle del movimiento: ', error);
      }
    });
  }
});