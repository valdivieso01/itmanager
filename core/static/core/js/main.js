function printDiv(nombreDiv) {
       var contenido= document.getElementById(nombreDiv).innerHTML;
       var contenidoOriginal= document.body.innerHTML;

   document.body.innerHTML = contenido;

       window.print();

       document.body.innerHTML = contenidoOriginal;
}

$("#main").click(function() {
  $("#mini-fab").toggleClass('hidden');
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();  
});

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

$(document).ready(function () {
  var trigger = $('.hamburger'),
      overlay = $('.overlay'),
     isClosed = false;

    trigger.click(function () {
      hamburger_cross();
    });

    function hamburger_cross() {

      if (isClosed == true) {
        overlay.hide();
        trigger.removeClass('is-open');
        trigger.addClass('is-closed');
        isClosed = false;
      } else {
        overlay.show();
        trigger.removeClass('is-closed');
        trigger.addClass('is-open');
        isClosed = true;
      }
  }

  $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
  });
});

