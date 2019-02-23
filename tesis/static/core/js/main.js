function printDiv(nombreDiv) {
       var contenido= document.getElementById(nombreDiv).innerHTML;
       var contenidoOriginal= document.body.innerHTML;

   document.body.innerHTML = contenido;

       window.print();

       document.body.innerHTML = contenidoOriginal;
}
$('.collapse').collapse()

$("#main").click(function() {
  $("#mini-fab").toggleClass('hidden');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();  
});
$.material.init();

$().ready(function () {
  $('.modal.printable').on('shown.bs.modal', function () {
      $('.modal-dialog', this).addClass('focused');
      $('body').addClass('modalprinter');

      if ($(this).hasClass('autoprint')) {
          window.print();
      }
  }).on('hidden.bs.modal', function () {
      $('.modal-dialog', this).removeClass('focused');
      $('body').removeClass('modalprinter');
  });
});
